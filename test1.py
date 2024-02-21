# import psycopg2
# from config import load_config

# def connect(config):
#     """Connect to the postgresql database server"""
#     try:
#         # connecting to the postgresql server
#         with psycopg2.connect(**config) as conn:
#             print('Connected to the postgresql server.')
#             return conn
#     except (psycopg2.DatabaseError, Exception) as error:
#         print(error)