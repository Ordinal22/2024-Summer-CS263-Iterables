import pytest
from hamcrest import assert_that, equal_to, has_property, has_string, is_, none, not_

from essay_question import EssayQuestion


def test_all_fields_present():
    question = EssayQuestion("Python Class Checklist")

    assert_that(question, has_property("question_text"))
    assert_that(question, has_property("feedback_correct"))
    assert_that(question, has_property("feedback_incorrect"))
    assert_that(question, has_property("points"))


def test_default_values():
    question = EssayQuestion("Python!!!!")

    assert_that(question.question_text, is_(equal_to("Python!!!!")))
    assert_that(question.feedback_correct, is_(none()))
    assert_that(question.feedback_incorrect, is_(none()))
    assert_that(question.points, is_(equal_to(0)))


def test_eq():
    lhs = EssayQuestion("Python!!!!")
    rhs = EssayQuestion("Rust!!!!")

    assert_that(lhs, is_(not_((equal_to(rhs)))))

    rhs.question_text = "Python!!!!"
    assert_that(lhs, is_((equal_to(rhs))))

    rhs.feedback_correct = "Correct!"
    assert_that(lhs, is_((equal_to(rhs))))

    rhs.feedback_incorrect = "Wrong... Python is not C++"
    assert_that(lhs, is_((equal_to(rhs))))

    rhs.points = 9001
    assert_that(lhs, is_((equal_to(rhs))))


def test_repr():
    question = EssayQuestion("Python!!!!")
    question.feedback_correct = "Correct!"
    question.feedback_incorrect = "Wrong... Python is not C++"
    question.points = 9001

    expected_str = "\n".join(
        (
            "EssayQuestion(",
            '    question_text="Python!!!!",',
            '    feedback_correct="Correct!",',
            '    feedback_incorrect="Wrong... Python is not C++",',
            "    points=9001",
            ")",
        )
    )

    assert_that(repr(question), is_(equal_to(expected_str)))


def test_str():
    question = EssayQuestion("Python!!!!")
    question.feedback_correct = "Correct!"
    question.feedback_incorrect = "Wrong... Python is not Java"
    question.points = 9001

    expected_str = "\n".join(
        (
            "Points: 9001",
            "",
            "Python!!!!",
            "",
            "Feedback:",
            "",
            "    Correct:",
            "        Correct!",
            "",
            "    Incorrect:",
            "        Wrong... Python is not Java",
        )
    )

    assert_that(question, has_string(expected_str))
