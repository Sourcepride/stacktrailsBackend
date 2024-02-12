import os
from requests_oauthlib import OAuth2Session
from .models import SocialAccount, User
from .choices import SocialChoices


class GithubAppStrategy:
    object_ = None

    def __init__(self) -> None:
        self.client_id = os.getenv("GITHUB_CLIENT_ID", None)
        self.client_secret = os.getenv("GITHUB_CLIENT_SECRET", None)
        if not self.client_id and not self.client_secret:
            raise ValueError("GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET must be set")
        self.oauthHandler = OAuth2Session(self.client_id)

        self.authorization_base_url = "https://github.com/login/oauth/authorize"
        self.token_url = "https://github.com/login/oauth/access_token"

    def get_full_client_authorization_url(self, request):
        extra_kwargs = {}
        callback_url = os.getenv("GITHUB_CALLBACK_URL")

        if callback_url:
            extra_kwargs["redirect_uri"] = callback_url

        authorization_url, _ = self.oauthHandler.authorization_url(
            self.authorization_base_url
        )

        return authorization_url

    def process_callback_information(self, url: str, request):
        self.oauthHandler.fetch_token(
            self.token_url, client_secret=self.client_secret, authorization_response=url
        )

        resp = self.oauthHandler.get(
            "https://api.github.com/user",
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

        if resp.ok:
            data = resp.json()
            query = SocialAccount.objects.filter(social_id=str(data.get("id")))
            if not query.exists():
                user, _ = User.objects.get_or_create(email=data.get("email"))
                SocialAccount.objects.create(
                    user=user,
                    id=str(data.get("id")),
                    avatar=str(data.get("avatar_url")),
                    provider=SocialChoices.GITHUB,
                )
                return user

            return query.first().user
        return

    @classmethod
    def get_or_create_object(cls):
        if not cls.object_:
            cls.object_ = GithubAppStrategy()
        return cls.object_
