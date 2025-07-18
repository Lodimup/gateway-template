import hashlib
import random
from typing import Literal

from appaccount.models.accounts import Account, User
from appaccount.models.auths import Session
from appcore.services.gen_token import gen_token
from ninja.security import HttpBearer


# fmt: off
def gen_random_username():
    """Generate a random username in the format 'adjective-animal-someHash'."""
    adjectives = [
        "absurd", "antique", "bouncy", "bubbly", "clumsy", "comical", "crazy", "daffy", "dizzy", "eccentric",
        "fancy", "flaky", "fluffy", "funky", "giddy", "giggly", "goofy", "groovy", "hilarious", "hysterical",
        "jolly", "jovial", "juicy", "kooky", "loony", "ludicrous", "merry", "mirthful", "nutty", "odd",
        "outrageous", "peppy", "perky", "potty", "pranky", "quirky", "ridiculous", "silly", "snazzy", "sneaky",
        "snoopy", "spiffy", "squirmy", "tacky", "tasty", "teasing", "tickleish", "tipsy", "toothy", "trendy",
        "twisty", "wacky", "waggish", "whacky", "whimsical", "wiggly", "wonky", "zany", "zippy", "zoomy",
        "blabby", "boingy", "boogly", "boppy", "bouncy", "bubbly", "bumpy", "bushy", "buzzy", "chirpy",
        "chubby", "clappy", "clippy", "clumsy", "cranky", "creepy", "crispy", "crunchy", "curly", "daffy",
        "dangly", "dinky", "dodgy", "dopey", "dorky", "droopy", "flappy", "floppy", "fluffy", "freaky",
        "frizzy", "frosty", "frothy", "fruity", "fudgy", "funky", "furry", "fuzzy", "giggly", "gloopy",
        "glossy", "goofy", "gory", "grainy", "greasy", "gritty", "groggy", "groovy", "grubby", "grumpy"
    ]
    animals = [
        "aardvark", "alpaca", "baboon", "badger", "beaver", "blobfish", "booby", "chicken", "chinchilla", "chipmunk",
        "cockatoo", "dingo", "dodo", "dugong", "dungbeetle", "ferret", "flamingo", "flea", "flicker", "gazelle",
        "gecko", "gerbil", "gibbon", "gnat", "gnu", "goose", "gopher", "gorilla", "grizzly", "hedgehog",
        "hippo", "hoopoe", "hyena", "ibex", "iguana", "impala", "jackal", "jaguar", "jellyfish", "kangaroo",
        "kiwi", "koala", "kookaburra", "lemur", "leopard", "llama", "lobster", "lynx", "macaw", "manatee",
        "meerkat", "mole", "mongoose", "monkey", "moose", "narwhal", "newt", "ocelot", "octopus", "opossum",
        "orangutan", "ostrich", "otter", "owl", "ox", "panda", "panther", "parrot", "peacock", "pelican",
        "penguin", "platypus", "porcupine", "porpoise", "prairie-dog", "puffin", "quail", "quokka", "rabbit", "raccoon",
        "rhino", "salamander", "seahorse", "seal", "serval", "shark", "skunk", "sloth", "snail", "snake",
        "squirrel", "starfish", "stingray", "stork", "swan", "tapir", "tarsier", "termite", "tiger", "toad",
        "toucan", "turtle", "vulture", "walrus", "wombat", "woodpecker", "yak", "zebra", "zebu"
    ]

    adjective = random.choice(adjectives)
    adjective2 = random.choice(adjectives)
    animal = random.choice(animals)
    some_hash = hashlib.sha256(
        str(random.getrandbits(256)).encode("utf-8")
    ).hexdigest()[:6]

    return f"{adjective}-{adjective2}-{animal}-{some_hash}"
# fmt: on


def create_session(uid: str, provider: Literal["google"], email: str | None) -> Session:
    """This is a function to login through service. It creates a session, and a user if not exist.

    Args:
        uid (str): user id
        provider (str): provider
        email (str): email

    Returns:
        Session: session object
    """
    account = Account.objects.filter(provider_account_id=uid).first()
    if account is None:
        username = gen_random_username()
        user = User.objects.create_user(
            username=username,
            email=email,
            password=gen_token(16),
        )
        account = Account.objects.create(
            user=user,
            provider=provider,
            provider_account_id=uid,
        )
    else:
        user = account.user

    session: Session = Session.objects.create(user=user)

    return session


class BearerTokenAuth(HttpBearer):
    """Authenticate using user's access_token."""

    def authenticate(self, request, token) -> Session | None:
        """This is a function to authenticate the token.

        Args:
            request (HttpRequest): request object
            token (str): token

        Returns:
            Session: session object
        """
        session: Session | None = Session.objects.filter(access_token=token).first()
        if session is None:
            return None
        if session.is_expired():
            return None

        return session


class ABearerTokenAuth(HttpBearer):
    """Authenthicate using user's access_token."""

    async def authenticate(self, request, token) -> Session | None:
        """This is a function to authenticate the token.

        Args:
            request (HttpRequest): request object
            token (str): token

        Returns:
            Session: session object
        """
        session: Session | None = (
            await Session.objects.filter(access_token=token)
            .select_related("user")
            .afirst()
        )
        if session is None:
            return None
        if session.is_expired():
            return None

        return session
