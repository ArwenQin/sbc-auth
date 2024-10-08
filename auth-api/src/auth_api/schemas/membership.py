# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Manager for membership schema and export."""

from marshmallow import fields

from auth_api.models import Membership as MembershipModel

from .base_schema import BaseSchema


class MembershipSchema(BaseSchema):  # pylint: disable=too-many-ancestors, too-few-public-methods
    """This is the schema for the Membership model."""

    class Meta(BaseSchema.Meta):  # pylint: disable=too-few-public-methods
        """Maps all of the Membership fields to a default schema."""

        model = MembershipModel
        fields = ("id", "membership_type_code", "user", "org", "membership_status", "membership_type")

    user = fields.Nested(
        "UserSchema", only=("firstname", "lastname", "username", "modified", "contacts", "login_source", "id")
    )
    org = fields.Nested("OrgSchema", only=("id", "name", "affiliated_entities", "org_type", "members", "invitations"))
    membership_status = fields.Pluck("MembershipStatusCodeSchema", "name", data_key="membershipStatus")
    membership_type = fields.Pluck("MembershipTypeSchema", "code", data_key="membershipType")
