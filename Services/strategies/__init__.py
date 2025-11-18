from .no_session import NoSessionStrategy
from .duplicate import DuplicateStrategy
from .expired import ExpiredStrategy
from .voted import VotedStrategy
from .completed import CompletedStrategy
from .error import ErrorStrategy

VOTE_STRATEGIES = {
    "no_session": NoSessionStrategy(),
    "duplicate": DuplicateStrategy(),
    "expired": ExpiredStrategy(),
    "voted": VotedStrategy(),
    "completed": CompletedStrategy(),
    "error": ErrorStrategy(),
}
