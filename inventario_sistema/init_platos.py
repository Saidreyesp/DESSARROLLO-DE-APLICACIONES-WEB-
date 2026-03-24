"""Script de inicialización para agregar platos a la base de datos con imágenes"""

from app import app, db
from inventario.productos import Producto

def init_platos():
    """Inicializa la base de datos con platos ecuatorianos típicos"""
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        # Platos nuevos que deseamos asegurar estén en la BD
        platos = [
            {
                'nombre': 'Guatita',
                'precio': 8.50,
                'cantidad': 15,
                'categoria': 'Platos Principales',
                'descripcion': 'Plato tradicional ecuatoriano hecho con tripa, papa y maní. Delicioso y nutritivo.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Guatita.jpg/640px-Guatita.jpg'
            },
            {
                'nombre': 'Asados',
                'precio': 12.00,
                'cantidad': 20,
                'categoria': 'Platos Principales',
                'descripcion': 'Carnes a la brasa marinadas en especias tradicionales. Jugosas y sabrosas.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/GrillFresh.jpg/640px-GrillFresh.jpg'
            },
            {
                'nombre': 'Seco de Gallina',
                'precio': 9.75,
                'cantidad': 18,
                'categoria': 'Platos Principales',
                'descripcion': 'Gallina cocinada en salsa de cilantro, cerveza y especias. Acompañado con arroz.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Seco_de_pollo.jpg/640px-Seco_de_pollo.jpg'
            },
            {
                'nombre': 'Seco de Carne',
                'precio': 10.50,
                'cantidad': 22,
                'categoria': 'Platos Principales',
                'descripcion': 'Res en guiso con cilantro, cebolla y especias. Acompañado con arroz y plátano.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Beef_stew.jpg/640px-Beef_stew.jpg'
            },
            {
                'nombre': 'Caldo de Gallina',
                'precio': 6.50,
                'cantidad': 25,
                'categoria': 'Sopas y Caldos',
                'descripcion': 'Caldo tradicional con gallina, verduras y hierbas aromáticas. Ideal para cualquier hora.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Chicken_soup.jpg/640px-Chicken_soup.jpg'
            },
            {
                'nombre': 'Caldo de Pata',
                'precio': 7.00,
                'cantidad': 20,
                'categoria': 'Sopas y Caldos',
                'descripcion': 'Caldo reconstituyente hecho con pata de res, maíz y especias. Excelente para la salud.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Beef_bone_broth.jpg/640px-Beef_bone_broth.jpg'
            },
            {
                'nombre': 'Pollo al Jugo',
                'precio': 8.25,
                'cantidad': 19,
                'categoria': 'Platos Principales',
                'descripcion': 'Pollo tierno cocido en su propio jugo con verduras. Acompañado con arroz y papas.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Cooked_chicken.jpg/640px-Cooked_chicken.jpg'
            },
            # nuevos
            {
                'nombre': 'Ceviche',
                'precio': 7.25,
                'cantidad': 30,
                'categoria': 'Entradas',
                'descripcion': 'Mezcla fresca de pescado o mariscos en jugo de limón con cebolla y cilantro.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Ceviche_de_pescado.jpg/640px-Ceviche_de_pescado.jpg'
            },
            {
                'nombre': 'Fritada',
                'precio': 11.00,
                'cantidad': 16,
                'categoria': 'Platos Principales',
                'descripcion': 'Piezas de cerdo fritas y sazonadas, servidas con mote y plátano.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Fritada_Ecuatoriana.jpg/640px-Fritada_Ecuatoriana.jpg'
            },
            {
                'nombre': 'Hornado',
                'precio': 13.50,
                'cantidad': 14,
                'categoria': 'Platos Principales',
                'descripcion': 'Cerdo asado lentamente hasta quedar dorado y jugoso, acompañado de llapingachos.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Hornado.jpg/640px-Hornado.jpg'
            },
            {
                'nombre': 'Churrasco',
                'precio': 12.75,
                'cantidad': 18,
                'categoria': 'Platos Principales',
                'descripcion': 'Bistec de res a la plancha servido con arroz, papas fritas y huevo frito.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Churrasco.jpg/640px-Churrasco.jpg'
            },
            {
                'nombre': 'Encebollado',
                'precio': 6.75,
                'cantidad': 25,
                'categoria': 'Sopas y Caldos',
                'descripcion': 'Sopa de pescado con yuca, cebolla encurtida y cilantro, típica de la costa.',
                'imagen': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Encebollado.jpg/640px-Encebollado.jpg'
            },
        ]
        
        # Agregar cada plato sin duplicados
        added = 0
        for plato_data in platos:
            # evitar inserciones repetidas buscando por nombre
            existing = Producto.query.filter_by(nombre=plato_data['nombre']).first()
            if existing:
                continue
            plato = Producto(**plato_data)
            db.session.add(plato)
            added += 1
        
        try:
            db.session.commit()
            print(f"\n✅ ¡ÉXITO! Se agregaron {added} platos nuevos a la base de datos:")
            print("-" * 60)
            for plato_data in platos:
                print(f"  • {plato_data['nombre']:20} - ${plato_data['precio']:6.2f} - {plato_data['categoria']}")
            print("-" * 60)
            print("\n💡 Tip: Ejecuta 'python app.py' para acceder a http://localhost:5000/menu")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error al agregar platos: {str(e)}")


if __name__ == '__main__':
    init_platos()
