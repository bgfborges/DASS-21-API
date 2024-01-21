"""
Test the App DB Models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Question, Answer, Report


class ModelTests(TestCase):
    """ Test Models """

    def test_create_user_with_email_successful(self):
        """ Test Create User with Email successful """

        email = 'test@example.com'
        password = 'testpassword'

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized(self):
        """ Normalize new users email """

        sample_emails = [
            ["test@EXAMPLE.com", "test@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            """ Test Normalized Data """

            user = get_user_model().objects.create_user(email, 'sample123')

            self.assertEqual(user.email, expected)

    def test_user_without_email_address(self):
        """ Test users without email address """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')

    def test_create_superuser(self):
        """ Test creating a superuser """

        email = 'test@example.com'
        password = 'testpassword'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class AnswerReportCreationTests(TestCase):
    """ Test Answer and Report Creation """

    def setUp(self):
        self.user = get_user_model().objects.create_user('test@example.com', 'sample123')
        self.question = Question.objects.create(
            text="How often do you feel stressed?",
            possible_answers=["Never", "Rarely", "Sometimes", "Always"]
        )
        self.value = 2

    def test_create_answer(self):
        """ Test creating an answer """
        answer = Answer.objects.create(
            user=self.user,
            question=self.question,
            value=self.value
        )

        self.assertEqual(answer.user, self.user)
        self.assertEqual(answer.question, self.question)
        self.assertEqual(answer.value, self.value)

    def test_create_report_with_answer(self):
        """ Test creating a report with an answer """
        answer = Answer.objects.create(
            user=self.user,
            question=self.question,
            value=self.value
        )

        report = Report.objects.create(
            user=self.user,
        )

        report.add_answer(answer)

        self.assertEqual(report.user, self.user)
        self.assertIn(answer, report.answers.all())

    def test_create_report_with_multiple_answers(self):
        """ Test creating a report with multiple answers """
        first_question = Question.objects.create(
            text="How often do you feel happy?",
            possible_answers=["Never", "Rarely", "Sometimes", "Always"]
        )
        first_value = 3

        second_question = Question.objects.create(
            text="How often do you feel anxious?",
            possible_answers=["Never", "Rarely", "Sometimes", "Always"]
        )
        second_value = 3

        first_answer = Answer.objects.create(
            user=self.user,
            question=first_question,
            value=first_value
        )

        second_answer = Answer.objects.create(
            user=self.user,
            question=second_question,
            value=second_value
        )

        report = Report.objects.create(
            user=self.user,
        )

        report.add_answer(first_answer)
        report.add_answer(second_answer)

        self.assertEqual(report.user, self.user)
        self.assertIn(first_answer, report.answers.all())
        self.assertIn(second_answer, report.answers.all())
