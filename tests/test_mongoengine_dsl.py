#!/usr/bin/env python
import unittest

from mongoengine import Document, Q, StringField, connect
from mongoengine_dsl import Query
from mongoengine_dsl.errors import InvalidSyntaxError, TransformHookError
from tests.utils import ts2dt


class DSLTest(unittest.TestCase):
    def test_whitespace(self):
        self.assertEqual(
            Q(key1='val1') & Q(key2='val2') & Q(key3='val3'),
            Query('key1:val1 and key2=val2 and key3==val3'),
        )
        self.assertEqual(
            Q(key1='val1') & Q(key2='val2') & Q(key3='val3'),
            Query('key1 : val1 and key2 = val2 and key3 == val3'),
        )

    def test_token(self):
        self.assertEqual(Q(key1='hi_there'), Query('key1: hi_there'))
        self.assertEqual(Q(key1='8a'), Query('key1: 8a'))
        self.assertEqual(Q(key1='8.8.'), Query('key1: 8.8.'))
        self.assertEqual(Q(key1='8.8.8'), Query('key1: 8.8.8'))
        self.assertEqual(Q(key1='8.8.8.8'), Query('key1: 8.8.8.8'))

    def test_quote_string(self):
        self.assertEqual(Q(key1='hi_there'), Query('key1: "hi_there"'))
        self.assertEqual(Q(key1='hi_there'), Query("key1: 'hi_there'"))
        self.assertEqual(Q(key1='hello world'), Query('key1: "hello world"'))
        self.assertEqual(Q(key1='hello world'), Query("key1: 'hello world'"))
        self.assertEqual(
            Q(key1='escape"this"world'),
            Query('key1: "escape\\"this\\"world"'),
        )
        self.assertEqual(
            Q(key1="escape'this'world"),
            Query("key1: 'escape\\'this\\'world'"),
        )

    def test_int(self):
        self.assertEqual(Q(key1=1), Query('key1:1'))
        self.assertEqual(Q(key1=-1), Query('key1:-1'))

    def test_float(self):
        self.assertEqual(Q(key1=1.213), Query('key1:1.213'))
        self.assertEqual(Q(key1=-1.213), Query('key1:-1.213'))

    def test_bool(self):
        self.assertEqual(
            Q(key1=True) & Q(key2=True) & Q(key3=True),
            Query('key1:true and key2:TRUE and key3:True'),
        )
        self.assertEqual(
            Q(key1=False) & Q(key2=False) & Q(key3=False),
            Query('key1:false and key2:FALSE and key3:False'),
        )

    def test_array(self):
        self.assertEqual(Q(key1=['hi']), Query('key1:[hi]'))
        self.assertEqual(
            Q(key1=[False, True, 1, 1.2, 'quote', 'no_quote']),
            Query('key1:[false, true, 1, 1.2, "quote", no_quote]'),
        )
        self.assertEqual(  # Full-width comma
            Q(key1=[False, True, 1, 1.2, 'quote', 'no_quote']),
            Query('key1:[false， true, 1， 1.2, "quote"， no_quote]'),
        )
        self.assertEqual(  # no comma
            Q(key1=[False, True, 1, 1.2, 'quote', 'no_quote']),
            Query('key1:[false true 1 1.2 "quote" no_quote]'),
        )
        self.assertEqual(Q(key1=[1, [2, 3]]), Query('key1:[1, [2, 3]]'))  # nested array
        self.assertEqual(  # nested more array
            Q(key1=[1, 2, [3, [4, 5, 6]]]),
            Query('key1:[1, 2, [3, [4, 5, 6]]]'),
        )
        self.assertRaisesRegex(
            InvalidSyntaxError,
            'Exclude operator cannot be used in arrays',
            Query,
            'key1 @ [!,2,3] and key2:"value2"',
        )
        self.assertRaisesRegex(
            InvalidSyntaxError,
            'Wildcard operator cannot be used in arrays',
            Query,
            'key1 !@ [*,2,3] and key2:"value2"',
        )

    def test_logical_priority(self):
        self.assertEqual(
            Q(key1='键1') & Q(key2='value2') & Q(键3='value3'),
            Query('key1:键1 and key2:"value2" and 键3:value3'),
        )
        self.assertEqual(
            (Q(key1='键1') | Q(key2='value2')) & Q(键3='value3'),
            Query('(key1:键1 or key2:"value2") and 键3:value3'),
        )
        self.assertEqual(
            Q(key1='键1') & (Q(key2='value2') | Q(键3='value3')),
            Query('key1:键1 and (key2:"value2" or 键3:value3)'),
        )
        self.assertEqual(
            Q(key1='键1') & (Q(key2='value2') | Q(键3='value3') | Q(key4='value4')),
            Query('key1:键1 and (key2:"value2" or 键3:value3 or key4: value4)'),
        )

    def test_equal(self):
        self.assertEqual(
            Q(key1='val1') & Q(key2='val2') & Q(key3='val3'),
            Query('key1:val1 and key2=val2 and key3==val3'),
        )
        self.assertEqual(
            Q(key1='val1') & Q(key2='val2') & Q(key3='val3'),
            Query('key1:val1 and key2=val2 and key3==val3'),
        )

    def test_not_equal(self):
        self.assertEqual(Q(key1__ne=1), Query('key1!=1'))

    def test_greater_than(self):
        self.assertEqual(Q(key1__gt=1), Query('key1>1'))
        self.assertEqual(Q(key1__gte=1), Query('key1>=1'))

    def test_less_than(self):
        self.assertEqual(Q(key1__lt=1), Query('key1<1'))
        self.assertEqual(Q(key1__lte=1), Query('key1<=1'))

    def test_exists_and_not_exists(self):
        self.assertEqual(
            Q(key1__exists=True) & Q(key2='value2'),
            Query('key1:* and key2:"value2"'),
        )
        self.assertEqual(
            Q(key1__exists=False) & Q(key2='value2'),
            Query('key1:! and key2:"value2"'),
        )
        self.assertRaisesRegex(
            InvalidSyntaxError,
            'Wildcard operator can only be used for equals',
            Query,
            'key1 != *',
        )
        self.assertRaisesRegex(
            InvalidSyntaxError,
            'Exclude operator can only be used for equals',
            Query,
            'key1 != !',
        )

    def test_contain_and_not_contain(self):
        self.assertEqual(
            Q(key1__in=[1, 2, 3]) & Q(key2='value2'),
            Query('key1 @ [1,2,3] and key2:"value2"'),
        )
        self.assertEqual(
            Q(key1__nin=[1, 2, 3]) & Q(key2='value2'),
            Query('key1 !@ [1,2,3] and key2:"value2"'),
        )

    def test_transform_hook(self):
        self.assertEqual(
            Q(key1=ts2dt(0)) & Q(key2=0),
            Query('key1: 0 and key2: 0', transform={'key1': ts2dt}),
        )
        self.assertEqual(  # bypass :*
            Q(key1__exists=True) & Q(key2=0),
            Query('key1: * and key2: 0', transform={'key1': ts2dt}),
        )
        self.assertEqual(  # bypass :!
            Q(key1__exists=False) & Q(key2=0),
            Query('key1: ! and key2: 0', transform={'key1': ts2dt}),
        )
        self.assertEqual(  # nested field
            Q(nested__key1=ts2dt(0)) & Q(key2=0),
            Query('nested.key1: 0 and key2: 0', transform={'nested.key1': ts2dt}),
        )
        self.assertRaisesRegex(  # hook exception handle
            TransformHookError,
            'Field key1 transform hook error',
            Query,
            'key1 != abc',
            transform={'key1': ts2dt},
        )

    def test_nested_field(self):
        self.assertEqual(Q(key__inner=0), Query('key.inner: 0'))


class OtherTest(unittest.TestCase):
    def test_readme_example(self):
        connect('mongoengine_test', host='mongomock://localhost')

        class User(Document):
            fullname = StringField()

        User(fullname='Tom').save()
        User(fullname='Dick').save()
        User(fullname='Harry').save()

        self.assertEqual(User.objects(Query('fullname: Dick')).first().fullname, 'Dick')
        self.assertEqual(
            User.objects(
                Query('fullname: dick', transform={'fullname': lambda x: x.title()})
            )
            .first()
            .fullname,
            'Dick',
        )
