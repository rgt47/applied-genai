#!/usr/bin/env python3
"""Weekly Mollick Substack refresh.

Fetches new posts from One Useful Thing since the cutoff recorded in
docs/mollick-digest.md, asks Claude to map each to a chapter and assess
chapter-affecting impact, writes a dated refresh file, updates the master
digest, appends BibTeX entries, and emails a summary.

Run as: python scripts/mollick_refresh.py

Required env vars:
  ANTHROPIC_API_KEY    -- Claude API access
  SMTP_USERNAME        -- Gmail address for outbound mail
  SMTP_PASSWORD        -- Gmail app password (not main password)
  NOTIFY_EMAIL         -- recipient address
"""

from __future__ import annotations

import json
import os
import re
import smtplib
import sys
from datetime import date, datetime, timezone
from email.message import EmailMessage
from pathlib import Path
from typing import Any

import requests
from anthropic import Anthropic

REPO_ROOT = Path(__file__).resolve().parent.parent
DIGEST = REPO_ROOT / 'docs' / 'mollick-digest.md'
BIB = REPO_ROOT / 'references.bib'
ARCHIVE_API = 'https://www.oneusefulthing.org/api/v1/archive'
USER_AGENT = (
  'mollick-refresh-bot (rgt47/applied-genai; weekly refresh)'
)

CHAPTERS = {
  'Ch1': 'Generative AI Landscape',
  'Ch2': 'Reasoning Models, Context, Verification',
  'Ch3': 'Biomedical RAG',
  'Ch4': 'Synthetic Data and Privacy',
  'Ch5': 'Multimodal Medical AI',
  'Ch6': 'Agents, Tool Use, MCP',
  'Ch7': 'Deep Research and Evidence Synthesis',
  'Ch8': 'Evaluation Beyond the Benchmark',
  'Ch9': 'Safety, Bias, Red-Teaming',
  'Ch10': 'Regulation, Privacy, IRB',
  'Ch11': 'Customisation and Adoption',
  'Ch12': 'Deployment',
  'XC': 'Cross-cutting',
  'NR': 'Not relevant',
}

ANALYSIS_PROMPT = """You are reviewing a new Ethan Mollick post for
relevance to a graduate biostatistics textbook,
*Applied Generative AI for Public Health and Biostatistics*. The book
has 12 chapters:

{chapters}

Read the post below and return a JSON object with these keys:
  chapter_code: one of {codes}
  rationale: one sentence on why this chapter
  summary: 100-150 words faithful to the post
  load_bearing_claim: a direct quote (under 30 words) that captures the
    single most citable observation
  impact: one of HIGH, MEDIUM, LOW. HIGH means the post would change a
    chapter's framing, scope, or section structure. MEDIUM means the post
    adds material warranting an Exercise or Further Reading entry. LOW
    means the post is a citation candidate only.
  impact_recommendation: if HIGH or MEDIUM, one sentence on what to
    revise; if LOW, the empty string.

Return ONLY the JSON object, no preamble.

POST TITLE: {title}
POST DATE: {date}
POST URL: {url}

POST CONTENT:
{content}
"""


def load_existing_cutoff() -> str:
  '''Find the most recent post date already recorded in the digest.'''
  if not DIGEST.exists():
    return '2024-05-01'
  content = DIGEST.read_text(encoding='utf-8')
  dates = re.findall(r'\| (20\d\d-\d\d-\d\d) \|', content)
  if not dates:
    return '2024-05-01'
  return max(dates)


def fetch_archive() -> list[dict[str, Any]]:
  '''Page through the Substack archive JSON API.'''
  headers = {'User-Agent': USER_AGENT}
  posts: list[dict[str, Any]] = []
  for offset in (0, 12, 24, 36, 48, 60):
    params = {'sort': 'new', 'offset': offset, 'limit': 12}
    response = requests.get(
      ARCHIVE_API, params=params, headers=headers, timeout=30
    )
    response.raise_for_status()
    chunk = response.json()
    if not chunk:
      break
    posts.extend(chunk)
    if len(chunk) < 12:
      break
  return posts


def filter_new(
  posts: list[dict[str, Any]], cutoff: str
) -> list[dict[str, Any]]:
  '''Keep posts published strictly after the cutoff date.'''
  out = []
  for post in posts:
    date_str = (post.get('post_date') or '')[:10]
    if date_str and date_str > cutoff:
      out.append(post)
  return sorted(out, key=lambda p: p['post_date'])


def fetch_post_text(url: str) -> str:
  '''Fetch the rendered post HTML and strip to text.'''
  response = requests.get(
    url, headers={'User-Agent': USER_AGENT}, timeout=30
  )
  response.raise_for_status()
  html = response.text
  text = re.sub(r'<script[\s\S]*?</script>', ' ', html)
  text = re.sub(r'<style[\s\S]*?</style>', ' ', text)
  text = re.sub(r'<[^>]+>', ' ', text)
  text = re.sub(r'\s+', ' ', text)
  return text[:18000]


def analyse_post(
  client: Anthropic, post: dict[str, Any]
) -> dict[str, Any]:
  '''Send the post to Claude and parse the JSON analysis.'''
  url = post.get('canonical_url') or post.get('url')
  prompt = ANALYSIS_PROMPT.format(
    chapters='\n'.join(
      f'  {code}: {name}' for code, name in CHAPTERS.items()
    ),
    codes=', '.join(CHAPTERS.keys()),
    title=post.get('title', ''),
    date=(post.get('post_date') or '')[:10],
    url=url,
    content=fetch_post_text(url),
  )
  msg = client.messages.create(
    model='claude-opus-4-7',
    max_tokens=2000,
    messages=[{'role': 'user', 'content': prompt}],
  )
  raw = msg.content[0].text.strip()
  match = re.search(r'\{[\s\S]*\}', raw)
  if not match:
    raise ValueError(f'No JSON in response: {raw[:200]}')
  return json.loads(match.group(0))


def write_refresh_file(
  today: str,
  cutoff: str,
  analyses: list[tuple[dict[str, Any], dict[str, Any]]],
) -> Path:
  '''Write the dated refresh file. Created even if zero new posts.'''
  out_path = REPO_ROOT / 'docs' / f'refresh-{today}.md'
  lines: list[str] = []
  lines.append(f'# Mollick refresh {today}')
  lines.append('')
  lines.append(
    f'_Cutoff: {cutoff}. New posts: {len(analyses)}._'
  )
  lines.append('')

  if not analyses:
    lines.append('No new posts since the previous cutoff.')
    out_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return out_path

  high = [a for _, a in analyses if a.get('impact') == 'HIGH']
  medium = [a for _, a in analyses if a.get('impact') == 'MEDIUM']
  low = [a for _, a in analyses if a.get('impact') == 'LOW']
  lines.append(
    f'_Impact distribution: {len(high)} HIGH, '
    f'{len(medium)} MEDIUM, {len(low)} LOW._'
  )
  lines.append('')

  if high or medium:
    lines.append('## Chapter-affecting shifts')
    lines.append('')
    for post, analysis in analyses:
      if analysis.get('impact') in ('HIGH', 'MEDIUM'):
        title = post.get('title', '')
        rec = analysis.get('impact_recommendation', '')
        code = analysis.get('chapter_code', 'XC')
        lines.append(
          f'- **{analysis["impact"]} ({code}): {title}** -- {rec}'
        )
    lines.append('')

  lines.append('## Post-by-post')
  lines.append('')
  for post, analysis in analyses:
    title = post.get('title', '')
    post_date = (post.get('post_date') or '')[:10]
    url = post.get('canonical_url') or post.get('url')
    code = analysis.get('chapter_code', 'XC')
    rationale = analysis.get('rationale', '')
    summary = analysis.get('summary', '')
    claim = analysis.get('load_bearing_claim', '')
    impact = analysis.get('impact', 'LOW')
    lines.append(f'### {post_date}: {title}')
    lines.append('')
    lines.append(f'- URL: <{url}>')
    lines.append(f'- Chapter: **{code}** -- {rationale}')
    lines.append(f'- Impact: **{impact}**')
    lines.append('')
    lines.append(summary)
    lines.append('')
    lines.append(f'> {claim}')
    lines.append('')

  out_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
  return out_path


def append_to_digest(
  analyses: list[tuple[dict[str, Any], dict[str, Any]]],
) -> None:
  '''Append new rows to the archive table in the master digest.'''
  if not analyses:
    return
  if not DIGEST.exists():
    return
  current = DIGEST.read_text(encoding='utf-8')
  rows = []
  for post, analysis in analyses:
    title = post.get('title', '')
    post_date = (post.get('post_date') or '')[:10]
    url = post.get('canonical_url') or post.get('url')
    code = analysis.get('chapter_code', 'XC')
    rows.append(f'| {post_date} | {title} | <{url}> | {code} |')

  marker = '## Distribution by chapter'
  if marker in current:
    parts = current.split(marker, 1)
    appended = parts[0].rstrip() + '\n' + '\n'.join(rows) + '\n\n' + (
      marker + parts[1]
    )
  else:
    appended = current.rstrip() + '\n' + '\n'.join(rows) + '\n'
  DIGEST.write_text(appended, encoding='utf-8')


def append_to_bib(
  analyses: list[tuple[dict[str, Any], dict[str, Any]]],
) -> None:
  '''Append BibTeX entries for new Mollick posts.'''
  if not analyses:
    return
  if not BIB.exists():
    return
  entries: list[str] = []
  for post, _ in analyses:
    title = post.get('title', '').replace('{', '').replace('}', '')
    post_date = (post.get('post_date') or '')[:10]
    year = post_date[:4] if post_date else 'n.d.'
    url = post.get('canonical_url') or post.get('url')
    slug = re.sub(r'[^a-z0-9]+', '_', title.lower()).strip('_')
    short = slug.split('_')[0] if slug else 'post'
    key = f'mollick_{year}_{short}'
    today = date.today().isoformat()
    entries.append(
      f'@misc{{{key},\n'
      f'  author = {{Mollick, Ethan}},\n'
      f'  title = {{{title}}},\n'
      f'  howpublished = {{One Useful Thing (Substack)}},\n'
      f'  year = {{{year}}},\n'
      f'  url = {{{url}}},\n'
      f'  urldate = {{{today}}}\n'
      f'}}'
    )
  with BIB.open('a', encoding='utf-8') as fh:
    fh.write('\n\n' + '\n\n'.join(entries) + '\n')


def send_email(
  refresh_file: Path,
  analyses: list[tuple[dict[str, Any], dict[str, Any]]],
  today: str,
) -> None:
  '''Send a summary email via Gmail SMTP.'''
  user = os.environ.get('SMTP_USERNAME')
  pwd = os.environ.get('SMTP_PASSWORD')
  to_addr = os.environ.get('NOTIFY_EMAIL')
  if not (user and pwd and to_addr):
    print('SMTP credentials not configured; skipping email')
    return
  subject = f'Mollick refresh {today}: {len(analyses)} new posts'
  body_lines = [
    f'Mollick refresh complete for {today}.',
    f'New posts: {len(analyses)}',
    '',
    f'See {refresh_file.name} in the repo for the full digest.',
    '',
  ]
  if analyses:
    high = [
      a for _, a in analyses if a.get('impact') == 'HIGH'
    ]
    if high:
      body_lines.append(f'HIGH-impact posts ({len(high)}):')
      for post, analysis in analyses:
        if analysis.get('impact') == 'HIGH':
          body_lines.append(
            f'  - {analysis.get("chapter_code", "XC")}: '
            f'{post.get("title", "")}'
          )

  msg = EmailMessage()
  msg['Subject'] = subject
  msg['From'] = user
  msg['To'] = to_addr
  msg.set_content('\n'.join(body_lines))
  with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(user, pwd)
    smtp.send_message(msg)
  print(f'Email sent to {to_addr}')


def main() -> int:
  api_key = os.environ.get('ANTHROPIC_API_KEY')
  if not api_key:
    print('ANTHROPIC_API_KEY missing; cannot run analysis', file=sys.stderr)
    return 1
  client = Anthropic(api_key=api_key)
  today = datetime.now(timezone.utc).date().isoformat()
  cutoff = load_existing_cutoff()
  print(f'Cutoff: {cutoff}; today: {today}')
  archive = fetch_archive()
  print(f'Archive size: {len(archive)}')
  new = filter_new(archive, cutoff)
  print(f'New posts: {len(new)}')

  analyses: list[tuple[dict[str, Any], dict[str, Any]]] = []
  for post in new:
    try:
      analysis = analyse_post(client, post)
      analyses.append((post, analysis))
      print(
        f'  {post.get("post_date", "")[:10]}: '
        f'{post.get("title", "")} -> '
        f'{analysis.get("chapter_code")} '
        f'({analysis.get("impact")})'
      )
    except Exception as exc:
      print(
        f'  Failed on {post.get("title", "")}: {exc}',
        file=sys.stderr,
      )

  refresh_file = write_refresh_file(today, cutoff, analyses)
  append_to_digest(analyses)
  append_to_bib(analyses)
  try:
    send_email(refresh_file, analyses, today)
  except Exception as exc:
    print(f'Email failed: {exc}', file=sys.stderr)
  print(f'Refresh file: {refresh_file}')
  return 0


if __name__ == '__main__':
  sys.exit(main())
