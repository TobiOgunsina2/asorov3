"""
language_cms/admin.py

The CMS is a bespoke interface — we do NOT register models here.
Standard Django admin is used for other models only.

To prevent ContentArchitect users from seeing Django admin at all,
ensure they are NOT is_staff=True. The CMS is their only interface.
"""
