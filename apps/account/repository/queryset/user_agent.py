from django.db.models import QuerySet
from django.db.models import F
from knox.models import AuthToken


class UserAgentQuerySet(QuerySet):
    def save_user_agent(self, user_agnet, token_id):
        self.create(user_agent=user_agnet, auth_token=token_id)

    def delete_all_user_agent(self, user_agent):
        digest_objs = self.filter(user_agent=user_agent). \
            annotate(dig=F('auth_token__digest')).values('dig')
        AuthToken.objects.filter(
            digest__in=[digest_obj['dig']
                        for digest_obj in digest_objs]).delete()

    def update_user_agent(self, user_agent, token_id):
        self.filter(auth_token=token_id).update(user_agent=user_agent)
