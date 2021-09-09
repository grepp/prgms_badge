from django.http.response import Http404, HttpResponseNotFound
import requests

from django.utils.timezone import datetime
from django.http import HttpResponse

from public_profile.models import PublicProfile

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 120

HEIGHT_PER_LINE = 10

BASE_URL = 'https://programmers.co.kr/api/job_profiles/public/'

def dark_profile(request, cover_name):
  width = DEFAULT_WIDTH
  height = DEFAULT_HEIGHT

  public_profile = get_public_profile(cover_name)
  
  if public_profile == None:
    return HttpResponseNotFound()

  primary_tags_svg, y_lines = get_primary_tags_svg(public_profile.primary_tags.names())

  height += 30 if y_lines > 0 else 0

  secondary_tags_svg, y_lines = get_secondary_tags_svg(public_profile.secondary_tags.names(), y_lines > 0)

  height += 30 + y_lines * HEIGHT_PER_LINE if y_lines > 0 else 0

  svg = get_svg(width, height, public_profile.email, public_profile.name, primary_tags_svg, secondary_tags_svg, 'dark')

  response = HttpResponse(content=svg)
  response['Content-Type'] = 'image/svg+xml'
  response['Cache-Control'] = 'no-cache'
  return response


def light_profile(request, cover_name):
  width = DEFAULT_WIDTH
  height = DEFAULT_HEIGHT

  public_profile = get_public_profile(cover_name)
  
  if public_profile == None:
    return HttpResponseNotFound()

  primary_tags_svg, y_lines = get_primary_tags_svg(public_profile.primary_tags.names())

  height += 30 if y_lines > 0 else 0

  secondary_tags_svg, y_lines = get_secondary_tags_svg(public_profile.secondary_tags.names(), y_lines > 0)

  height += 30 + y_lines * HEIGHT_PER_LINE if y_lines > 0 else 0

  svg = get_svg(width, height, public_profile.email, public_profile.name, primary_tags_svg, secondary_tags_svg, 'light')

  response = HttpResponse(content=svg)
  response['Content-Type'] = 'image/svg+xml'
  response['Cache-Control'] = 'no-cache'
  return response

def get_svg(width, height, email, name, primary_tags_svg, secondary_tags_svg, version):
  main_rect_style = 'fill:#0c151c;' if version == 'dark' else 'fill:#fff;stroke-width:0.15rem;stroke:#d7e2eb;'
  main_text_color = '#fff' if version == 'dark' else '#000'

  return '''
    <svg height="{height}" width="{width}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
      <defs>
        <style>
          .main-rect {{
            {main_rect_style}
          }}
          .name-text {{
            font-size:36px;
            font-weight: 600;
          }}
          .name-text,.email-text,.primary_tag-title,.secondary-tag-rect {{
            fill:{main_text_color};
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
          .email-text {{
            font-size:14px;
            font-family:HelveticaNeue-Medium, Helvetica Neue;
          }}
          .cls-5 {{
            letter-spacing:-0.02em;
          }}
          .primary_tag-title {{
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
      <g>
        <g>
          <rect class="main-rect" width="{width}" height="{height}" rx="14"/>
          <text class="name-text" transform="translate(22.88 48.22)">
            {name}
          </text>
          <g id="icons">
            <g id="ic-email-14">
              <path id="path" class="cls-3" d="M26.85,64.4H34a1.43,1.43,0,0,1,1.43,1.43v5.71A1.43,1.43,0,0,1,34,73H26.85a1.43,1.43,0,0,1-1.43-1.43V65.83A1.43,1.43,0,0,1,26.85,64.4Zm7.85,2.5-4.28,2.86L26.13,66.9V65.83l4.29,2.86,4.28-2.86Z"/>
            </g>
          </g>
          <text class="email-text" transform="translate(43.98 72.52)">
            {email}
          </text>
          {primary_tags_svg}
          {secondary_tags_svg}
        </g>
      </g>
    </svg>
  '''.format(
    main_rect_style=main_rect_style,
    main_text_color=main_text_color,
    width=width,
    height=height,
    email=email,
    name=name,
    primary_tags_svg=primary_tags_svg,
    secondary_tags_svg=secondary_tags_svg,
  )

def get_public_profile(cover_name):
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
      return None
  return public_profile

def get_primary_tags_svg(tags):
  RECT_START_X = 25.33
  RECT_START_Y = 105
  MARGIN_BETWEEN_TAG = 3
  RECT_RX = 3

  rect_x = RECT_START_X
  rect_y = RECT_START_Y
  rect_height = 16
  y_lines = 1

  if len(tags) > 0:
    ret = '<text class="primary_tag-title" transform="translate(25.26 95.73)">주요 기술</text>'
  else:
    ret = ''
    y_lines = 0

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

  return (ret, y_lines)

def get_secondary_tags_svg(tags, is_primary_tags_exist):
  RECT_START_X = 25.33
  TITLE_TEXT_Y = 136.97 if is_primary_tags_exist else 106.97
  RECT_START_Y = 145 if is_primary_tags_exist else 115
  MAX_X = 350
  MARGIN_BETWEEN_TAG = 3
  RECT_RX = 3

  rect_x = RECT_START_X
  rect_y = RECT_START_Y
  rect_height = 16
  y_lines = 1

  if len(tags) > 0:
    ret = '<text class="primary_tag-title" transform="translate(25.39 {y})">기술 태그</text>'.format(y=TITLE_TEXT_Y)
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
