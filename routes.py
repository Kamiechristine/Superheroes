from flask import jsonify, request
from models import db, Hero, Power, HeroPower

def setup_routes(app):
    @app.route('/heroes', methods=['GET'])
    def get_heroes():
        heroes = Hero.query.all()
        return jsonify([{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes])

    @app.route('/heroes/<int:id>', methods=['GET'])
    def get_hero(id):
        hero = Hero.query.get(id)
        if hero:
            return jsonify({
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "hero_powers": [{
                    "hero_id": hp.hero_id,
                    "id": hp.id,
                    "power": {
                        "description": hp.power.description,
                        "id": hp.power.id,
                        "name": hp.power.name
                    },
                    "power_id": hp.power_id,
                    "strength": hp.strength
                } for hp in hero.hero_powers]
            })
        return jsonify({"error": "Hero not found"}), 404

    @app.route('/powers', methods=['GET'])
    def get_powers():
        powers = Power.query.all()
        return jsonify([{"id": power.id, "name": power.name, "description": power.description} for power in powers])

    @app.route('/powers/<int:id>', methods=['GET'])
    def get_power(id):
        power = Power.query.get(id)
        if power:
            return jsonify({
                "id": power.id,
                "name": power.name,
                "description": power.description
            })
        return jsonify({"error": "Power not found"}), 404

    @app.route('/powers/<int:id>', methods=['PATCH'])
    def update_power(id):
        power = Power.query.get(id)
        if not power:
            return jsonify({"error": "Power not found"}), 404

        data = request.get_json()
        if 'description' in data:
            power.description = data['description']
            db.session.commit()
            return jsonify({
                "id": power.id,
                "name": power.name,
                "description": power.description
            })
        return jsonify({"errors": ["validation errors"]}), 400

    @app.route('/hero_powers', methods=['POST'])
    def create_hero_power():
        data = request.get_json()
        new_hero_power = HeroPower(
            strength=data['strength'],
            power_id=data['power_id'],
            hero_id=data['hero_id']
        )
        db.session.add(new_hero_power)
        db.session.commit()
        return jsonify({
            "id": new_hero_power.id,
            "hero_id": new_hero_power.hero_id,
            "power_id": new_hero_power.power_id,
            "strength": new_hero_power.strength,
            "hero": {
                "id": new_hero_power.hero.id,
                "name": new_hero_power.hero.name,
                "super_name": new_hero_power.hero.super_name
            },
            "power": {
                "id": new_hero_power.power.id,
                "name": new_hero_power.power.name,
                "description": new_hero_power.power.description
            }
        })
