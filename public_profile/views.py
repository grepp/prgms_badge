from django.shortcuts import render
from django.http import HttpResponse

def dark_profile(request, cover_name):
  width = 400
  height = 200

  name = 'Koa'
  email = 'koa@grepp.co'
  primary_tags = ['Ruby on rails', 'Python3', 'C++']
  secondary_tags = ['C', 'test', 'test22', 'test22', 'test22', 'test22', 'test22', 'test22', 'test22', 'test22', 'test22', 'test22']

  primary_tags_svg = get_primary_tags_svg(primary_tags)

  secondary_tags_svg = get_secondary_tags_svg(secondary_tags)

  svg = '''
    <svg height="{height}" width="{width}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
      <defs>
        <style>
          .cls-1 {{
            fill:#0c151c;
          }}
          .cls-2 {{
            font-size:36px;
          }}
          .cls-2,.cls-4,.cls-6,.secondary-tag-rect {{
            fill:#fff;
          }}
          .primary-tag-rect {{
            fill:#fff;
          }}
          .secondary-tag-rect {{
            fill:#E9ECF3;
          }}
          .cls-2,.tag-text {{
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
          .tag-text {{
            font-size: 11px;
          }}
        </style>
      </defs>
      <g id="레이어_2" data-name="레이어 2">
        <g id="레이어_1-2" data-name="레이어 1">
          <rect class="cls-1" width="{width}" height="{height}" rx="14"/>
          <text class="cls-2" transform="translate(22.88 48.22)">
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
          <text class="cls-6" transform="translate(25.39 136.97)">
            기술 태그
          </text>
          {secondary_tags_svg}
        </g>
      </g>
    </svg>
  '''.format(
    width=width,
    height=height,
    email=email,
    name=name,
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
  rect_height = 15


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

    text_svg = '<text class="tag-text" text-anchor="middle" transform="translate({x} {y})">{tag}</text>'.format(
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
  rect_height = 15

  ret = ''

  for tag in tags:
    width = get_tag_rect_width_by_tag_str(tag)

    if rect_x + width > MAX_X:
      rect_x = RECT_START_X
      rect_y = rect_y + rect_height + MARGIN_BETWEEN_TAG

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
    

  return ret


def get_tag_rect_width_by_tag_str(tag: str):
  default_width = 10
  len_blank = tag.count(' ')
  len_without_blank = len(tag) - len_blank

  return default_width + len_blank + len_without_blank * 5.8