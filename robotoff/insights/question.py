import abc
from typing import Dict, List

from robotoff.insights._enum import InsightType
from robotoff.models import ProductInsight
from robotoff.utils import get_logger
from robotoff.utils.types import JSONType

logger = get_logger(__name__)


class Question(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def serialize(self) -> JSONType:
        pass

    @abc.abstractmethod
    def get_type(self):
        pass


class AddBinaryQuestion(Question):
    def __init__(self, question: str, value: str, insight: ProductInsight):
        self.question: str = question
        self.value: str = value
        self.insight_id: str = str(insight.id)
        self.insight_type: str = str(insight.type)

    def get_type(self):
        return 'add-binary'

    def serialize(self) -> JSONType:
        return {
            'type': self.get_type(),
            'value': self.value,
            'question': self.question,
            'insight_id': self.insight_id,
            'insight_type': self.insight_type,
        }


class QuestionFormatter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def format_question(self, insight: ProductInsight) -> Question:
        pass


class CategoryQuestionFormatter(QuestionFormatter):
    question = "category-question"

    def format_question(self, insight: ProductInsight) -> Question:
        return AddBinaryQuestion(question=self.question,
                                 value=insight.data['category'],
                                 insight=insight)


class QuestionFormatterFactory:
    formatters: Dict[str, type] = {
        InsightType.category.name: CategoryQuestionFormatter,
    }

    @classmethod
    def get(cls, insight_type: str):
        return cls.formatters.get(insight_type)

    @classmethod
    def get_available_types(cls) -> List[str]:
        return list(cls.formatters.keys())
