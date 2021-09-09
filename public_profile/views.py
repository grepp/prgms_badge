from django.http.response import Http404
import requests

from django.utils.timezone import datetime
from django.http import HttpResponse

from public_profile.models import PublicProfile

BASE_URL = 'https://programmers.co.kr/api/job_profiles/public/'

def dark_profile(request, cover_name):
  width = 400
  height = 150

  public_profile, created = PublicProfile.objects.get_or_create(cover_name = cover_name)

  if created or public_profile.updated_at.date() != datetime.today().date():
    url = BASE_URL + cover_name
    try:
      response = requests.get(url).json()
      resume = response['resume']

      public_profile.name = resume['name'] if 'name' in resume else ''
      public_profile.email = resume['email'] if 'email' in resume else ''
      
      public_profile.primary_tags.add(resume['primary_tags'] if 'primary_tags' in resume else [])
      public_profile.primary_tags.add(resume['secondary_tags'] if 'secondary_tags' in resume else [])

      public_profile.save()

    except:
      return Http404

  primary_tags_svg = get_primary_tags_svg(public_profile.primary_tags.names())

  secondary_tags_svg, y_lines = get_secondary_tags_svg(public_profile.secondary_tags.names())

  height += 30 + y_lines * 10 if y_lines > 0 else 0

  svg = '''
    <svg height="{height}" width="{width}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
      <defs>
        <style>
          .cls-1 {{
            fill:#0c151c;
          }}
          .name-text {{
            font-size:36px;
            font-weight: 600;
          }}
          .name-text,.cls-4,.cls-6,.secondary-tag-rect {{
            fill:#fff;
          }}
          .primary-tag-rect {{
            fill:#263747;
          }}
          .secondary-tag-rect {{
            fill:#E9ECF3;
          }}
          .name-text,.tag-text {{
            font-family:HelveticaNeue, Helvetica Neue;
          }}
          .cls-3 {{
            fill:#b2c0cc;fill-rule:evenodd;
          }}
          .cls-4 {{
            font-size:14px;
            font-family:HelveticaNeue-Medium, Helvetica Neue;
          }}
          .cls-5 {{
            letter-spacing:-0.02em;
          }}
          .cls-6 {{
            font-size:13px;
            font-family:SourceHanSansKR-Normal-KSCpc-EUC-H, Source Han Sans KR;
          }}
          .primary-tag-text {{
            fill: #FBFBFD;
          }}
          .tag-text {{
            font-size: 11px;
          }}
        </style>
      </defs>
      <g id="레이어_2" data-name="레이어 2">
        <g id="레이어_1-2" data-name="레이어 1">
          <rect class="cls-1" width="{width}" height="{height}" rx="14"/>
          <text class="name-text" transform="translate(22.88 48.22)">
            {name}
          </text>
          <g id="icons">
            <g id="ic-email-14">
              <path id="path" class="cls-3" d="M26.85,64.4H34a1.43,1.43,0,0,1,1.43,1.43v5.71A1.43,1.43,0,0,1,34,73H26.85a1.43,1.43,0,0,1-1.43-1.43V65.83A1.43,1.43,0,0,1,26.85,64.4Zm7.85,2.5-4.28,2.86L26.13,66.9V65.83l4.29,2.86,4.28-2.86Z"/>
            </g>
          </g>
          <text class="cls-4" transform="translate(43.98 72.52)">
            {email}
          </text>
          <text class="cls-6" transform="translate(25.26 95.73)">
            주요 기술
          </text>
          {primary_tags_svg}
          {secondary_tags_svg}
        </g>
      </g>
    </svg>
  '''.format(
    width=width,
    height=height,
    email=public_profile.email,
    name=public_profile.name,
    primary_tags_svg=primary_tags_svg,
    secondary_tags_svg=secondary_tags_svg,
  )

  response = HttpResponse(content=svg)
  response['Content-Type'] = 'image/svg+xml'
  response['Cache-Control'] = 'no-cache'
  return response


def light_profile(request, cover_name):
  width = 400
  height = 150

  public_profile, created = PublicProfile.objects.get_or_create(cover_name = cover_name)

  if created or public_profile.updated_at.date() != datetime.today().date():
    url = BASE_URL + cover_name
    try:
      response = requests.get(url).json()
      resume = response['resume']

      public_profile.name = resume['name'] if 'name' in resume else ''
      public_profile.email = resume['email'] if 'email' in resume else ''
      
      public_profile.primary_tags.add(resume['primary_tags'] if 'primary_tags' in resume else [])
      public_profile.primary_tags.add(resume['secondary_tags'] if 'secondary_tags' in resume else [])

      public_profile.save()

    except:
      return Http404

  primary_tags_svg = get_primary_tags_svg(public_profile.primary_tags.names())

  secondary_tags_svg, y_lines = get_secondary_tags_svg(public_profile.secondary_tags.names())

  height += 30 + y_lines * 10 if y_lines > 0 else 0

  svg = '''
    <svg height="{height}" width="{width}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
      <defs>
        <style>
          .cls-1 {{
            fill:#fff;
            stroke-width: .15rem;
            stroke:#d7e2eb;
          }}
          .name-text {{
            font-size:36px;
            font-weight: 600;
          }}
          .name-text,.cls-4,.cls-6,.secondary-tag-rect {{
            fill:#000;
          }}
          .primary-tag-rect {{
            fill:#263747;
          }}
          .secondary-tag-rect {{
            fill:#E9ECF3;
          }}
          .name-text,.tag-text {{
            font-family:HelveticaNeue, Helvetica Neue;
          }}
          .cls-3 {{
            fill:#b2c0cc;
            fill-rule:evenodd;
          }}
          .cls-4 {{
            font-size:14px;
            font-family:HelveticaNeue-Medium, Helvetica Neue;
          }}
          .cls-5 {{
            letter-spacing:-0.02em;
          }}
          .cls-6 {{
            font-size:13px;
            font-family:SourceHanSansKR-Normal-KSCpc-EUC-H, Source Han Sans KR;
          }}
          .primary-tag-text {{
            fill: #FBFBFD;
          }}
          .tag-text {{
            font-size: 11px;
          }}
        </style>
      </defs>
      <g id="레이어_2" data-name="레이어 2">
        <g id="레이어_1-2" data-name="레이어 1">
          <rect class="cls-1" width="{width}" height="{height}" rx="14"/>
          <text class="name-text" transform="translate(22.88 48.22)">
            {name}
          </text>
          <g id="icons">
            <g id="ic-email-14">
              <path id="path" class="cls-3" d="M26.85,64.4H34a1.43,1.43,0,0,1,1.43,1.43v5.71A1.43,1.43,0,0,1,34,73H26.85a1.43,1.43,0,0,1-1.43-1.43V65.83A1.43,1.43,0,0,1,26.85,64.4Zm7.85,2.5-4.28,2.86L26.13,66.9V65.83l4.29,2.86,4.28-2.86Z"/>
            </g>
          </g>
          <text class="cls-4" transform="translate(43.98 72.52)">
            {email}
          </text>
          <text class="cls-6" transform="translate(25.26 95.73)">
            주요 기술
          </text>
          {primary_tags_svg}
          {secondary_tags_svg}
        </g>
      </g>
    </svg>
  '''.format(
    width=width,
    height=height,
    email=public_profile.email,
    name=public_profile.name,
    primary_tags_svg=primary_tags_svg,
    secondary_tags_svg=secondary_tags_svg,
  )

  response = HttpResponse(content=svg)
  response['Content-Type'] = 'image/svg+xml'
  response['Cache-Control'] = 'no-cache'
  return response

def get_primary_tags_svg(tags):
  RECT_START_X = 25.33
  RECT_START_Y = 105
  MARGIN_BETWEEN_TAG = 3
  RECT_RX = 3


  rect_x = RECT_START_X
  rect_y = RECT_START_Y
  rect_height = 16


  ret = ''

  for tag in tags:
    width = get_tag_rect_width_by_tag_str(tag)
    rect_svg = '<rect class="primary-tag-rect" x="{x}" y="{y}" width="{width}" height="{height}" rx="{rx}"/>'.format(
      x = rect_x,
      y = rect_y,
      width = width,
      height=rect_height,
      rx = RECT_RX,
    )

    text_svg = '<text class="primary-tag-text tag-text" text-anchor="middle" transform="translate({x} {y})">{tag}</text>'.format(
      tag=tag,
      x = rect_x + width / 2,
      y = rect_y + rect_height * 2 / 3,
    )

    ret += rect_svg + text_svg  
    rect_x += width + MARGIN_BETWEEN_TAG 

  return ret

def get_secondary_tags_svg(tags):
  RECT_START_X = 25.33
  RECT_START_Y = 145
  MAX_X = 350
  MARGIN_BETWEEN_TAG = 3
  RECT_RX = 3

  rect_x = RECT_START_X
  rect_y = RECT_START_Y
  rect_height = 16
  y_lines = 1

  if len(tags) > 0:
    ret = '<text class="cls-6" transform="translate(25.39 136.97)">기술 태그</text>'
  else:
    ret = ''
    y_lines = 0


  for tag in tags:
    width = get_tag_rect_width_by_tag_str(tag)

    if rect_x + width > MAX_X:
      rect_x = RECT_START_X
      rect_y = rect_y + rect_height + MARGIN_BETWEEN_TAG
      y_lines += 1

    rect_svg = '<rect class="secondary-tag-rect" x="{x}" y="{y}" width="{width}" height="{height}" rx="{rx}"/>'.format(
      x = rect_x,
      y = rect_y,
      width = width,
      height=rect_height,
      rx = RECT_RX,
    )

    text_svg = '<text class="tag-text" text-anchor="middle" transform="translate({x} {y})">{tag}</text>'.format(
      tag=tag,
      x = rect_x + width / 2,
      y = rect_y + rect_height * 2 / 3,
    )

    ret += rect_svg + text_svg
    rect_x += width + MARGIN_BETWEEN_TAG

  return (ret, y_lines)


def get_tag_rect_width_by_tag_str(tag: str):
  default_width = 14
  len_blank = tag.count(' ')
  len_without_blank = len(tag) - len_blank

  return default_width + len_blank + len_without_blank * 6
