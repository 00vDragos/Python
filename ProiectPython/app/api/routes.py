from flask import Blueprint, request, jsonify
from ..services.math_service import MathService
from ..schemas.operations import (
    FibonacciRequest,
    PowRequest,
    FactorialRequest,
    LoginRequest,
)
from pydantic import ValidationError
from ..models.request_log import RequestLog
from ..models.user import User
from ..core.extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_cors import cross_origin

api_bp = Blueprint("api", __name__)
math_service = MathService()


@api_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"})


@api_bp.route("/fibonacci", methods=["POST"])
@jwt_required()
def calculate_fib():
    try:
        data = request.get_json(force=True)
        fib_request = FibonacciRequest(**data)

        if fib_request.n < 0:
            return jsonify({"error": "Numarul trebuie sa fie mai mare decat 0"}), 400

        result, from_cache = math_service.fib(fib_request.n)
        user_id = get_jwt_identity()

        log_entry = RequestLog(
            operation="fibonacci",
            input_data=f"n={fib_request.n}",
            result=str(result),
            user_id=user_id
        )
        db.session.add(log_entry)
        db.session.commit()

        return jsonify({"result": result, "from_cache": from_cache})

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422
    except Exception as e:
        print("Eroare server:", e)
        return jsonify({"error": "Eroare interna"}), 500


@api_bp.route("/factorial", methods=["POST"])
@jwt_required()
def calculate_factorial():
    try:
        data = request.get_json(force=True)
        print("Primit in /factorial:", data)

        if not isinstance(data, dict) or "n" not in data:
            return jsonify({"error": "Campul 'n' este necesar"}), 422

        fact_request = FactorialRequest(**data)
        if fact_request.n < 0:
            return jsonify({"error": "Numarul trebuie sa fie pozitiv"}), 400

        result, from_cache = math_service.factorial(fact_request.n)
        user_id = get_jwt_identity()

        log_entry = RequestLog(
            operation="factorial",
            input_data=f"n={fact_request.n}",
            result=str(result),
            user_id=user_id
        )
        db.session.add(log_entry)
        db.session.commit()

        return jsonify({"result": result, "from_cache": from_cache})

    except ValidationError as e:
        print("VALIDATION ERROR FACTORIAL:", e.errors())
        return jsonify({"error": e.errors()}), 422
    except Exception as e:
        print("UNEXPECTED ERROR FACTORIAL:", e)
        return jsonify({"error": str(e)}), 500


@api_bp.route("/pow", methods=["POST"])
@jwt_required()
def calculate_pow():
    try:
        data = request.get_json(force=True)
        print("Primit in /pow:", data)

        if not isinstance(data, dict) or "base" not in data or "exponent" not in data:
            return jsonify({"error": "Payload invalid"}), 422

        pow_request = PowRequest(**data)
        if pow_request.base < 0 or pow_request.exponent < 0:
            return jsonify({"error": "Numarul trebuie sa fie pozitiv"}), 400

        result, from_cache = math_service.pow(pow_request.base, pow_request.exponent)
        user_id = get_jwt_identity()

        log_entry = RequestLog(
            operation="pow",
            input_data=f"base={pow_request.base}, exponent={pow_request.exponent}",
            result=str(result),
            user_id=user_id
        )
        db.session.add(log_entry)
        db.session.commit()

        return jsonify({"result": result, "from_cache": from_cache})

    except ValidationError as e:
        print("Validation error pow:", e.errors())
        return jsonify({"error": e.errors()}), 422
    except Exception as e:
        print("Eroare neasteptata pow:", e)
        return jsonify({"error": str(e)}), 500


@api_bp.route("/login", methods=["POST"])
@cross_origin(origins="http://localhost:5173", supports_credentials=True)
def login():
    try:
        data = request.get_json()
        print("[LOGIN] Payload primit:", data)

        login_data = LoginRequest(**data)

        user = User.query.filter_by(email=login_data.email).first()
        if user and user.check_password(login_data.password):
            print("[LOGIN] Utilizator validat")
            access_token = create_access_token(identity=str(user.id))
            return jsonify({"access_token": access_token})
        else:
            print("[LOGIN] Date incorecte")
            return jsonify({"error": "Credentiale invalide"}), 401

    except ValidationError as e:
        print("[LOGIN] Eroare Pydantic:", e.errors())
        return jsonify({"error": e.errors()}), 422
    except Exception as e:
        print("[LOGIN] Eroare server:", e)
        return jsonify({"error": "Eroare server"}), 500


@api_bp.route("/register", methods=["POST"])
@cross_origin(origins="http://localhost:5173", supports_credentials=True)
def register():
    try:
        data = request.get_json()
        print("[REGISTER] Payload primit:", data)

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email si parola sunt obligatorii"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email deja inregistrat"}), 400

        user = User(email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Cont creat cu succes"}), 201

    except Exception as e:
        print("[REGISTER] Eroare:", e)
        db.session.rollback()
        return jsonify({"error": "Eroare interna"}), 500



