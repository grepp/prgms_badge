"""# public_profile.models.py
  - PublicProfile
"""
from django.db import models
from configs.models import BaseModel
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

class TaggedPrimaryTag(TaggedItemBase):
  content_object = models.ForeignKey(
    "PublicProfile",
    on_delete=models.CASCADE,
  )

class TaggedSecondaryTag(TaggedItemBase):
  content_object = models.ForeignKey(
    "PublicProfile",
    on_delete=models.CASCADE,
  )


class PublicProfile(BaseModel):
  """## PublicProfile
    - 과도한 API 호출을 막기 위해 캐쉬 데이터를 저장하는 모델입니다.
  """
  cover_name = models.TextField(
    blank=True,
    null=True,
    verbose_name='Cover name'
  )
  name = models.TextField(
    blank=True,
    null=True,
    verbose_name='이름'
  )
  email = models.TextField(
    blank=True,
    null=True,
    verbose_name='이메일'
  )
  primary_tags = TaggableManager(
    through=TaggedPrimaryTag,
    related_name='primary_tags',
    blank=True,
  )

  secondary_tags = TaggableManager(
    through=TaggedSecondaryTag,
    related_name='secondary_tags',
    blank=True,
  )
