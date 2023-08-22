from ariadne import ObjectType, MutationType, make_executable_schema, graphql_sync
from flask import Flask, request, jsonify
from threading import Thread
import hashlib
import logging

# Define the mutation
mutation = MutationType()

@mutation.field("hashData")
def hash_data_resolver(_, info, data):
    logging.debug("graphql mutation running Mutation.hash_data_resolver()")
    hash_object = hashlib.sha256(data.encode())
    logging.debug("graphqul mutation hash_object.hexdigest() = %s" % hash_object.hexdigest())
    hex_dig = hash_object.hexdigest()
    return hex_dig

# Define the schema
type_defs = """
    type Query {
        _empty: String
    }

    type Mutation {
        hashData(data: String!): String!
    }
"""

# Create the schema
schema = make_executable_schema(type_defs, mutation)

# Run the server in a separate thread
def initGQLServer():
    # Create the Flask app
    logging.info("Starting GraphQL server...")
    print(f"[+] Starting GraphQL server...")
    app = Flask(__name__)

    @app.route('/graphql', methods=['POST'])
    def graphql_server():
        data = request.get_json()
        success, result = graphql_sync(schema, data)
        status_code = 200 if success else 400
        return jsonify(result), status_code

    app.run(threaded=True, host="0.0.0.0", port=8081)
    logging.info("Stopping GraphQL server...")
    print("[!] Stopping GraphQL server...")
