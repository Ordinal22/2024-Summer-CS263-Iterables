from dataclasses import dataclass, field
from typing import Generator, Optional, Self

import pytest
from hamcrest import (
    assert_that,
    ends_with,
    equal_to,
    has_property,
    has_string,
    is_,
    none,
    not_,
    starts_with,
)

from essay_question import EssayQuestion
from question_pool import QuestionPool


@dataclass
class EssayBuilder:
    text: Optional[str] = field(default=None, init=False)
    correct: Optional[str] = field(default=None, init=False)
    incorrect: Optional[str] = field(default=None, init=False)
    points: int = field(default=0, init=False)

    def with_text(self, val: str) -> Self:
        self.text = val
        return self

    def with_feedback(
        self, *, correct: Optional[str] = None, incorrect: Optional[str] = None
    ) -> Self:
        self.correct = correct
        self.incorrect = incorrect
        return self

    def with_points(self, val: int) -> Self:
        self.points = val
        return self

    def build(self) -> EssayQuestion:
        if self.text is None:
            raise ValueError("'text' is required")

        question = EssayQuestion(self.text)
        question.feedback_correct = self.correct
        question.feedback_incorrect = self.incorrect
        question.points = self.points

        return question


def pad_left(the_str: str, *, spaces: int) -> str:
    """
    This is a utility function that adds a specified number of spaces at the
    start of a string.
    """

    return f"{' ' * spaces}{the_str}"


@pytest.fixture
def checklist_pools() -> (
    Generator[tuple[QuestionPool, QuestionPool, QuestionPool], None, None]
):
    cpp_pool = QuestionPool("C++ Class Checklist")
    java_pool = QuestionPool("Java Class Checklist")
    python_pool = QuestionPool("Python Class Checklist")

    yield cpp_pool, java_pool, python_pool


@pytest.fixture
def python_question_list() -> Generator[list[EssayQuestion], None, None]:
    yield [
        (
            EssayBuilder()
            .with_text("__eq__ is similar to Java's ____ method")
            .with_feedback(incorrect="equals is Java's logical equivalence function")
            .with_points(2)
            .build()
        ),
        (
            EssayBuilder()
            .with_text("__str__ is similar to Java's ____ method")
            .with_feedback(incorrect="toString is Java's pseudo-output function")
            .with_points(2)
            .build()
        ),
        (
            EssayBuilder()
            .with_text("__hash__ is similar to Java's ____ method")
            .with_feedback(incorrect="hashCode is Java's hashing function")
            .with_points(2)
            .build()
        ),
        (
            EssayBuilder()
            .with_text(
                "What Python mechanic is abused to provide pseudo-private attributes?"
            )
            .with_feedback(
                correct="Exactly!",
                incorrect="The '__' or name mangling mechanic is meant to avoid naming collisions",
            )
            .with_points(2)
            .build()
        ),
    ]


def test_all_fields_present():
    pool = QuestionPool("Rust Class Checklist")

    assert_that(pool, has_property("title"))
    assert_that(pool, has_property("questions"))


def test_default_values():
    with pytest.raises(TypeError):
        pool = QuestionPool()

    pool = QuestionPool("Rust Class Checklist")
    assert_that(pool.questions, is_(equal_to([])))


def test_eq_identity(checklist_pools):
    cpp_pool, java_pool, python_pool = checklist_pools

    current_pool = cpp_pool
    assert_that(current_pool, is_(equal_to(current_pool)))

    current_pool = java_pool
    assert_that(current_pool, is_(equal_to(current_pool)))

    current_pool = python_pool
    assert_that(current_pool, is_(equal_to(current_pool)))


def test_eq_are_equal(python_question_list):
    src_questions = python_question_list

    pool_1 = QuestionPool("Python Checklist")
    pool_2 = QuestionPool("Python Checklist")

    assert_that(pool_1, is_(equal_to(pool_2)))

    pool_1.questions.append(src_questions[0])
    assert_that(pool_1, is_(not_(equal_to(pool_2))))

    pool_2.questions.append(src_questions[0])
    assert_that(pool_1, is_(equal_to(pool_2)))

    pool_1.questions.append(src_questions[1])
    pool_1.questions.append(src_questions[2])
    pool_1.questions.append(src_questions[3])

    pool_2.questions.append(src_questions[1])
    pool_2.questions.append(src_questions[2])
    pool_2.questions.append(src_questions[3])

    assert_that(pool_1, is_(equal_to(pool_2)))


def test_eq_not_equal(checklist_pools, python_question_list):
    cpp_pool, java_pool, python_pool = checklist_pools
    src_questions = python_question_list

    assert_that(cpp_pool, is_(not_(equal_to(python_pool))))
    assert_that(java_pool, is_(not_(equal_to(python_pool))))

    pool_1 = QuestionPool("Python Checklist")
    pool_2 = QuestionPool("Python Checklist")

    assert_that(pool_1, is_(equal_to(pool_2)))

    pool_1.questions.append(src_questions[0])
    assert_that(pool_1, is_(not_(equal_to(pool_2))))

    pool_2.questions.append(src_questions[0])
    assert_that(pool_1, is_(equal_to(pool_2)))

    pool_1.questions.append(src_questions[1])
    pool_1.questions.append(src_questions[2])
    pool_1.questions.append(src_questions[3])

    pool_2.questions.append(src_questions[3])
    pool_2.questions.append(src_questions[1])
    pool_2.questions.append(src_questions[2])

    assert_that(pool_1, is_(not_(equal_to(pool_2))))


def test_iter_empty():
    pool = QuestionPool("Rust Class Checklist")

    with pytest.raises(StopIteration):
        next(iter(pool))


def test_iter(python_question_list):
    src_questions = python_question_list

    pool_1 = QuestionPool("Python Checklist")

    pool_1.questions.append(src_questions[0])
    pool_1.questions.append(src_questions[1])
    pool_1.questions.append(src_questions[3])
    pool_1.questions.append(src_questions[2])

    it = iter(pool_1)

    assert_that(next(it), is_(equal_to(src_questions[0])))
    assert_that(next(it), is_(equal_to(src_questions[1])))
    assert_that(next(it), is_(equal_to(src_questions[3])))
    assert_that(next(it), is_(equal_to(src_questions[2])))

    with pytest.raises(StopIteration):
        next(it)


def test_repr(python_question_list):
    src_questions = python_question_list

    question_block = ",\n".join(repr(question) for question in src_questions)
    padded_block = "\n".join(
        pad_left(line, spaces=8) for line in question_block.splitlines()
    )

    expected_block = "\n".join(
        (
            "QuestionPool(",
            f'    title="Python Checklist",',
            "    questions=[",
            padded_block,
            "    ]",
            ")",
        )
    )

    pool = QuestionPool("Python Checklist")
    for question in src_questions:
        pool.questions.append(question)

    assert_that(repr(pool), starts_with("QuestionPool("))
    assert_that(repr(pool), ends_with(")"))
    assert_that(repr(pool), is_(equal_to(expected_block)))
