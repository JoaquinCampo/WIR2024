import unittest
from unittest.mock import patch
from redditAPI import buscarPublicaciones

class TestBuscarPublicaciones(unittest.TestCase):

    @patch('redditAPI.rq.get')
    def test_successful_fetch(self, mock_get):
        # Mock response
        response_json = {
            'data': {
                'children': [
                    {
                        'data': {
                            'id': 'post1',
                            'name': 'Post 1',
                            'title': 'Title 1',
                            'selftext': 'Text 1'
                        }
                    },
                    {
                        'data': {
                            'id': 'post2',
                            'name': 'Post 2',
                            'title': 'Title 2',
                            'selftext': 'Text 2'
                        }
                    }
                ],
                'after': 'next_post_id'
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = response_json

        # Call the function
        posts, next_post_id = buscarPublicaciones('entity', None)

        # Assertions
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0]['id'], 'post1')
        self.assertEqual(posts[0]['name'], 'Post 1')
        self.assertEqual(posts[0]['title'], 'Title 1')
        self.assertEqual(posts[0]['text'], 'Text 1')
        self.assertEqual(posts[1]['id'], 'post2')
        self.assertEqual(posts[1]['name'], 'Post 2')
        self.assertEqual(posts[1]['title'], 'Title 2')
        self.assertEqual(posts[1]['text'], 'Text 2')
        self.assertEqual(next_post_id, 'next_post_id')

    @patch('redditAPI.rq.get')
    def test_failed_fetch(self, mock_get):
        # Mock response
        response_json = {
            'error': 'Failed to fetch data'
        }
        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = response_json

        # Call the function
        result = buscarPublicaciones('entity', None)

        # Assertions
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()