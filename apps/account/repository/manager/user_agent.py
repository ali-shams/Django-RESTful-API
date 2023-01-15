from django.db.models import Manager

from apps.account.repository.queryset import UserAgentQuerySet


class UserAgentDataAccessLayerManager(Manager):
    def get_queryset(self):
        return UserAgentQuerySet(self.model, using=self._db)

    def save_user_agent(self, user_agnet, token_id):
        return self.get_queryset().save_user_agent(user_agnet, token_id)

    def delete_all_user_agent(self, user_agent):
        return self.get_queryset().delete_all_user_agent(user_agent)

    def update_user_agent(self, user_agent, token_id):
        return self.get_queryset().update_user_agent(user_agent, token_id)

