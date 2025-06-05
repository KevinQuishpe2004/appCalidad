from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os
from datetime import datetime

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    
    # Import models here to avoid circular imports
    from models.user import User
    from models.posture import Posture
    from models.therapy_type import TherapyType
    from models.series import Series
    from models.series_posture import SeriesPosture
    from models.session import Session
    
    with app.app_context():
        db.create_all()

def populate_initial_data():
    from models.user import User
    from models.posture import Posture
    from models.therapy_type import TherapyType
    
    # Check if data already exists
    if TherapyType.query.first() is not None:
        return
    
    # Create therapy types
    therapy_types = [
        TherapyType(name="Dolor de Cabeza", description="Posturas para ayudar a aliviar el dolor de cabeza y reducir la tensión."),
        TherapyType(name="Insomnio", description="Posturas diseñadas para promover la relajación y mejorar la calidad del sueño."),
        TherapyType(name="Mala Postura", description="Posturas para corregir la postura y fortalecer la columna vertebral.")
    ]
    
    db.session.add_all(therapy_types)
    db.session.commit()
    
    # Create demo admin user if no users exist
    if User.query.first() is None:
        admin = User(
            username="admin",
            password=generate_password_hash("admin123"),
            email="admin@example.com",
            name="Administrator",
            role="instructor"
        )
        db.session.add(admin)
        db.session.commit()
    
    # Add sample postures
    # anxiety_poses = dolorCabeza_poses
    dolorCabeza_poses = [
        {"name": "Child", "sanskrit_name": "Balasana", "image_url": "https://i.blogs.es/bdffc3/1366_2000-8-/1366_521.jpeg", 
         "description": "Una postura relajante que calma el cerebro y ayuda a aliviar el estrés y la ansiedad.", 
         "steps": "Póngase a cuatro patas. \nSiéntate sobre los talones y apoya la cabeza en la esterilla. \nColoca los brazos a los lados. \nCon cada exhalación relaja todo el cuerpo.", 
         "benefits": "Calma la mente, alivia el estrés y la fatiga, ayuda a aliviar los dolores de espalda y cuello.", 
         "modifications": "Aleje los dedos del cuerpo para estirar caderas, muslos y tobillos."},
        
        {"name": "Cat", "sanskrit_name": "Matwork", "image_url": "https://kavaalya.com/wp-content/uploads/2023/10/postura-gato-marjaryasana.jpg", 
         "description": "Un movimiento fluido y terapéutico que mejora la flexibilidad de la columna vertebral, libera tensiones y masajea los órganos abdominales.", 
         "steps": "Arrodillarse a cuatro patas. Manos alineadas con los hombros. \nLos dedos apuntan hacia delante. Rodillas por debajo de las caderas. \nRedondear la espalda hacia arriba. \nMete el estómago. Dejar caer la cabeza. \nPausa arriba. Levanta las nalgas. Curvar la columna hacia abajo. \nVuelva al principio y repita.", 
         "benefits": "Ayuda a la espalda y los glúteos. Ejercicio de liberación muscular. Lubrica el giro.", 
         "modifications": "Levantar la pierna hacia un lado (perro haciendo pis)."},
        
        {"name": "Classical Fish", "sanskrit_name": "VMatsyasana", "image_url": "https://s3.ppllstatics.com/mujerhoy/www/multimedia/202206/21/media/cortadas/Matsyasana%20(1)-kN2D-U170491754246IBD-1248x1248@MujerHoy.jpeg", 
         "description": "Una postura rejuvenecedora que abre el pecho, estimula la garganta y mejora la respiración, mientras libera tensiones en la columna vertebral. Ideal para contrarrestar los efectos de estar sentado mucho tiempo.", 
         "steps": "Siéntese erguido. Extienda las piernas (postura del bastón). \nCon la ayuda de las manos, coloque el pie derecho sobre el muslo izquierdo y el pie izquierdo sobre el muslo derecho. \nFlexione la espalda sobre los codos hasta que la parte superior de la cabeza toque el suelo. \nSujete los dedos de los pies con las manos y arquee la espalda. \nSostener. Soltar.", 
         "benefits": "Estira muslos, rodillas y tobillos.", 
         "modifications": "No modificaciones necesarias."},
        
        {"name": "Prostration", "sanskrit_name": "Naman Pranamasana", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfPCJnVmUjpnwUIkBHGOPyjavxUXE98MU_yA-AEAeZrZIoPl_XFOrEe0gqkIVmfXZVf6g&usqp=CAU", 
         "description": "Una postura de reverencia profunda que combina flexión hacia adelante y ligera inversión, promoviendo humildad, calma mental y estiramiento suave de la columna vertebral.", 
         "steps": "Siéntese sobre las rodillas (Vajrasana).\n Sujete la parte inferior de las pantorrillas. Inclínese hacia delante. \nColoque la coronilla en el suelo, delante de las rodillas. Levante las nalgas hasta que los muslos estén verticales.\n Presione suavemente la barbilla contra el pecho. Mantenga la posición.", 
         "benefits": "Activar el tronco. Preparación para pararse de cabeza y de hombros.", 
         "modifications": "Parada de cabeza."},
        
        {"name": "Aham Prema Mantra", "sanskrit_name": "Mantras", "image_url": "https://previews.123rf.com/images/inarik/inarik1503/inarik150300047/37386181-yoga-woman-in-meditation-sitting-in-lotus-pose-female-meditating-exercise-isolated-over-white.jpg", 
         "description": "Un poderoso mantra de origen sánscrito que significa 'Yo soy Amor Divino'. Su repetición consciente activa la vibración del amor puro, conectando el corazón con la conciencia universal. Ideal para meditación, sanación emocional y cultivo de compasión.", 
         "steps": "Siéntate cómodamente con la espalda recta, cierra los ojos, respira profundo y repite en silencio o en voz alta “Aham Prema” durante varios minutos con atención plena.", 
         "benefits": "Mejora de la concentración. Reducción del estrés. Autoconocimiento. Curación emocional. Refuerzo del sistema inmunitario. Aumento de los niveles de energía. Práctica espiritual más profunda.", 
         "modifications": "A) Siéntate sobre un cojín, una manta doblada o un bloque. \n B) Sentarse contra una pared.\n  C) Sentarse en una silla. \n D) Cambiar el cruce de las piernas. \n E) Siéntate en la postura del Héroe, del Perfecto o del Loto."},
        
        {"name": "Camel Wide Legs", "sanskrit_name": "Ustrasana", "image_url": "https://www.hola.com/horizon/landscape/777472627dce-ustrasana-t.jpg?im=Resize=(360),type=downsize", 
         "description": "Una poderosa flexión hacia atrás que abre el corazón y las caderas, combinando los beneficios de Ustrasana con un mayor estímulo para los músculos internos de los muslos y la pelvis. Ideal para contrarrestar el encorvamiento y mejorar la respiración profunda.", 
         "steps": "Arrodíllese con las piernas abiertas. \nApoye las manos en la parte posterior de la pelvis. Señale con los dedos hacia abajo. \nInclínese hacia atrás. Mentón cerca del esternón.\n Apoyar las palmas de las manos en los talones. Los pliegues de los codos miran hacia delante. \n Para salir, llevar una mano a la vez a las caderas. Levante la cabeza y el torso empujando los puntos de las caderas hacia abajo.", 
         "benefits": "Estira tobillos, muslos, ingles, abdominales, pecho, garganta, psoas.", 
         "modifications": "Las palmas contra las plantas."}
    ]
    
    insomnio_poses = [
        {"name": "Crocodile", "sanskrit_name": "Makarasana", "image_url": "https://images.ctfassets.net/p0sybd6jir6r/s9dGpWThHitnXPvqDrN5Q/e8fb4534d33ca3139176433156e2713a/Crocodile_Pose_1-4d14c71073ed4be3409dec347a112d6f.jpg?w=1600&fm=webp&q=70", 
         "description": "Una postura restaurativa que relaja profundamente el cuerpo, alivia la tensión en la espalda y favorece una respiración tranquila y consciente.", 
         "steps": "Relájese sobre el estómago. Brazos cruzados en el suelo por encima de la cabeza. Abrir las piernas.\n Girar los pies para que los talones apunten hacia dentro. Apretar los glúteos. Presione la pelvis contra el suelo. Apoyar la frente en los brazos.", 
         "benefits": "Estira espalda, piernas y glúteos. Reduce el estrés. Mejora la postura.", 
         "modifications": "Coloque la frente en Yoni Mudra."},
        
        {"name": "Locust", "sanskrit_name": "Salabhasana", "image_url": "https://cdn.yogajournal.com/wp-content/uploads/2022/03/locust-pose_andrew-clark.jpg", 
         "description": "Un estiramiento completo que fortalece la espalda, activa los isquiotibiales y abre los hombros, mejorando la postura y la energía.", 
         "steps": "Túmbate boca abajo. Pies juntos. La frente en el suelo. Coloque los brazos a los lados. Las palmas hacia arriba. Estire la barbilla ligeramente hacia delante. Apoyar la barbilla en el suelo. Suavizar la parte delantera del cuerpo. Levante el pecho, las piernas y los brazos del suelo. Extienda las puntas de los dedos de las manos hacia los pies. Mirar al frente.", 
         "benefits": "Tonifica los músculos de la espalda. Estimula la zona lumbar.", 
         "modifications": "1 pierna arriba. Piernas anchas. Manos debajo del cuerpo, a los lados o delante."},
        
        {"name": "Prostration", "sanskrit_name": "Naman Pranamasana", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfPCJnVmUjpnwUIkBHGOPyjavxUXE98MU_yA-AEAeZrZIoPl_XFOrEe0gqkIVmfXZVf6g&usqp=CAU", 
         "description": "Una postura de reverencia profunda que combina flexión hacia adelante y ligera inversión, promoviendo humildad, calma mental y estiramiento suave de la columna vertebral.", 
         "steps": "Siéntese sobre las rodillas (Vajrasana).\n Sujete la parte inferior de las pantorrillas. Inclínese hacia delante. \nColoque la coronilla en el suelo, delante de las rodillas. Levante las nalgas hasta que los muslos estén verticales.\n Presione suavemente la barbilla contra el pecho. Mantenga la posición.", 
         "benefits": "Activar el tronco. Preparación para pararse de cabeza y de hombros.", 
         "modifications": "Parada de cabeza."},
        
        {"name": "Child", "sanskrit_name": "Balasana", "image_url": "https://i.blogs.es/bdffc3/1366_2000-8-/1366_521.jpeg", 
         "description": "Una postura relajante que calma el cerebro y ayuda a aliviar el estrés y la ansiedad.", 
         "steps": "Póngase a cuatro patas. \nSiéntate sobre los talones y apoya la cabeza en la esterilla. \nColoca los brazos a los lados. \nCon cada exhalación relaja todo el cuerpo.", 
         "benefits": "Calma la mente, alivia el estrés y la fatiga, ayuda a aliviar los dolores de espalda y cuello.", 
         "modifications": "Aleje los dedos del cuerpo para estirar caderas, muslos y tobillos."},
        
        {"name": "Easy Ear To Shoulder I", "sanskrit_name": "Greeva Sanchalana", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5bNwoU3bXLK5ygb1AZIcPYRhMieq5m8tSx1bGXieqdrRvDgh6iZ1gZNszsgfg7WBK1Co&usqp=CAU", 
         "description": "Una postura suave que libera tensión en el cuello y mejora la movilidad cervical mediante estiramientos laterales conscientes.", 
         "steps": "Siéntate o ponte de pie. Cierre los ojos. \nMire directamente hacia delante. Relaje los hombros. \nMueva lentamente la cabeza hacia la derecha e intente tocar el hombro derecho con la oreja derecha (sin levantar los hombros). \nRepita en el otro lado.", 
         "benefits": "Flexibilidad en el cuello.", 
         "modifications": "A) Almohada bajo las nalgas. \nB) Espalda contra la pared. \nC) Palmas de las manos juntas en el centro del pecho. \nD) Dobla 1/4, 1/2 o 3/4 de la espalda hacia abajo. \nE) Entrelaza los dedos, extiende los brazos por encima de la cabeza, estírate hacia arriba y dóblate hacia delante."},
        
        {"name": "Bound Hand Headstand B", "sanskrit_name": "Baddha Hasta Sirsasana B", "image_url": "https://www.fitsri.com/wp-content/uploads/2021/01/bound-hands-headstand-1024x683.jpg", 
         "description": "Una postura invertida avanzada que fortalece el núcleo, mejora el equilibrio y revitaliza todo el cuerpo al estimular la circulación.", 
         "steps": "Siéntate sobre los talones. Extienda los brazos. \nDoble los codos y agarre el antebrazo opuesto por el codo. Coloque los antebrazos sobre la colchoneta y doble los dedos de los pies hacia abajo.\n Coloque la coronilla justo delante de los antebrazos. Empiece a presionar los antebrazos firmemente contra la esterilla mientras baja los hombros para alargar el cuello. \nManteniendo la presión en los antebrazos y el cuello largo, levante las rodillas y lleve los pies hacia la cabeza. \nColoque la rodilla derecha sobre el tríceps derecho. Coloque la rodilla izquierda sobre el tríceps izquierdo. \nLevante una pierna cada vez. Contraiga el tronco. Sujetar. Los codos sostienen la mayor parte del peso (no la cabeza ni el cuello). \nSi pierde el equilibrio, gire el cuerpo hacia delante. Para soltarse, ponga rápidamente las palmas de las manos en el suelo para mantener el equilibrio, doble la cintura y colóquese en plancha.", 
         "benefits": "El rey de las asanas. Piel brillante. Activa el núcleo.", 
         "modifications": "El rey de las asanas. Piel brillante. Parada de cabeza en Baddha Konasana, Parada de cabeza con piernas de águila. Parada de cabeza con piernas de loto. Parada de cabeza con Twisting Splits. Parada de cabeza con piernas anchas."}
    ]
    
    mala_postura_poses = [
        {"name": "Child", "sanskrit_name": "Balasana", "image_url": "https://i.blogs.es/bdffc3/1366_2000-8-/1366_521.jpeg", 
         "description": "Una postura relajante que calma el cerebro y ayuda a aliviar el estrés y la ansiedad.", 
         "steps": "Póngase a cuatro patas. Siéntate sobre los talones y apoya la cabeza en la esterilla.\n Coloca los brazos a los lados. Con cada exhalación relaja todo el cuerpo.", 
         "benefits": "Calma la mente, alivia el estrés y la fatiga, ayuda a aliviar los dolores de espalda y cuello.", 
         "modifications": "Aleje los dedos del cuerpo para estirar caderas, muslos y tobillos."},
        
        {"name": "Cat", "sanskrit_name": "Matwork", "image_url": "https://kavaalya.com/wp-content/uploads/2023/10/postura-gato-marjaryasana.jpg", 
         "description": "Un movimiento fluido y terapéutico que mejora la flexibilidad de la columna vertebral, libera tensiones y masajea los órganos abdominales.", 
         "steps": "Arrodillarse a cuatro patas. Manos alineadas con los hombros. \nLos dedos apuntan hacia delante. Rodillas por debajo de las caderas. \nRedondear la espalda hacia arriba. \nMete el estómago. Dejar caer la cabeza. \nPausa arriba. Levanta las nalgas. Curvar la columna hacia abajo. \nVuelva al principio y repita.", 
         "benefits": "Ayuda a la espalda y los glúteos. Ejercicio de liberación muscular. Lubrica el giro.", 
         "modifications": "Levantar la pierna hacia un lado (perro haciendo pis)."},
        
        {"name": "Abdominal Stretch", "sanskrit_name": "Udarakarshanasana", "image_url": "https://pranayoga.co.in/asana/wp-content/uploads/Udarakarshanasana%E2%80%93Abdominal-Stretch-Posture.jpg", 
         "description": "Una torsión en cuclillas que estimula la digestión, desintoxica el cuerpo y mejora la movilidad de la parte inferior del tronco.", 
         "steps": "Empezar en cuclillas estrechas (talones levantados si es necesario). Coloque las palmas de las manos delante de las rodillas. En la espiración, llevar la rodilla derecha al suelo a través de la línea media (hacia el pie izquierdo). \nGire el cuerpo hacia la izquierda. Mire hacia atrás.\n La rodilla izquierda permanece lo más quieta posible. Vuelva al centro. Repita del otro lado.", 
         "benefits": "Mejora la flexibilidad de caderas, rodillas y tobillos. Desintoxicación.", 
         "modifications": "Mientras caminas hacia delante, lleva la rodilla opuesta hacia o sobre el suelo."},
        
        {"name": "Alice In Wonderland", "sanskrit_name": "Tadasana", "image_url": "https://www.yogabasics.com/yogabasics2017/wp-content/uploads/2013/11/Tadasana_2280.jpg", 
         "description": "Una postura de pie fundamental que mejora el equilibrio, alinea la postura y activa todo el cuerpo con serenidad y firmeza.", 
         "steps": "Imagina que tienes una poción mágica que te dio Alicia en el País de las Maravillas.\n Bebe. ¡Vaya! Cada vez eres más alto (estira las manos sobre la cabeza).", 
         "benefits": "Equilibrio. Calmante. Mejora la postura. Fortalece las piernas. Refuerza el tronco.", 
         "modifications": "Manos en oración detrás de la espalda. Ojos cerrados."},
        
        {"name": "Base", "sanskrit_name": "Prarambhik Sthiti", "image_url": "https://wiki.yoga-vidya.de/images/thumb/f/ff/Grundhaltung_Prarambhik_Sthiti_bzw-_Parambhasana_-_Langsitz_-_Ausgangslage.jpg/250px-Grundhaltung_Prarambhik_Sthiti_bzw-_Parambhasana_-_Langsitz_-_Ausgangslage.jpg", 
         "description": "Una postura de descanso que calma la mente, alinea la columna y reduce el estrés al mantener el torso erguido y relajado.", 
         "steps": "Siéntate con las piernas extendidas. Pies juntos. \nPalmas detrás de las nalgas. Dedos hacia atrás. Los brazos sostienen el 20% del peso del torso.\n El otro 80% del peso del torso lo soportan la espalda y los músculos centrales (siente cómo la columna se hace más alta). \nMira al frente (o cierra los ojos).", 
         "benefits": "Fortalece los músculos de la espalda. Estira los hombros y el pecho.", 
         "modifications": "Siéntese sobre una manta doblada para levantar la pelvis. Espalda contra la pared."},
        
        {"name": "Crocodile", "sanskrit_name": "Makarasana", "image_url": "https://images.ctfassets.net/p0sybd6jir6r/s9dGpWThHitnXPvqDrN5Q/e8fb4534d33ca3139176433156e2713a/Crocodile_Pose_1-4d14c71073ed4be3409dec347a112d6f.jpg?w=1600&fm=webp&q=70", 
         "description": "Una postura restaurativa que relaja profundamente el cuerpo, alivia la tensión en la espalda y favorece una respiración tranquila y consciente.", 
         "steps": "Relájese sobre el estómago. Brazos cruzados en el suelo por encima de la cabeza.\n Abrir las piernas. Girar los pies para que los talones apunten hacia dentro. Apretar los glúteos. Presione la pelvis contra el suelo.\n Apoyar la frente en los brazos.", 
         "benefits": "Estira espalda, piernas y glúteos. Reduce el estrés. Mejora la postura.", 
         "modifications": "Coloque la frente en Yoni Mudra."}
    ]
    
    # Add therapy types to poses
    dolorCabeza_id = TherapyType.query.filter_by(name="Dolor de Cabeza").first().id
    insomnio_id = TherapyType.query.filter_by(name="Insomnio").first().id
    mala_postura_id = TherapyType.query.filter_by(name="Mala Postura").first().id
    
    for pose_data in dolorCabeza_poses:
        pose = Posture(
            name=pose_data["name"],
            sanskrit_name=pose_data["sanskrit_name"],
            image_url=pose_data["image_url"],
            description=pose_data["description"],
            steps=pose_data["steps"],
            benefits=pose_data["benefits"],
            modifications=pose_data["modifications"]
        )
        pose.therapy_types.append(TherapyType.query.get(dolorCabeza_id))
        db.session.add(pose)
    
    for pose_data in insomnio_poses:
        # Check if pose already exists
        existing_pose = Posture.query.filter_by(name=pose_data["name"]).first()
        if existing_pose:
            existing_pose.therapy_types.append(TherapyType.query.get(insomnio_id))
        else:
            pose = Posture(
                name=pose_data["name"],
                sanskrit_name=pose_data["sanskrit_name"],
                image_url=pose_data["image_url"],
                description=pose_data["description"],
                steps=pose_data["steps"],
                benefits=pose_data["benefits"],
                modifications=pose_data["modifications"]
            )
            pose.therapy_types.append(TherapyType.query.get(insomnio_id))
            db.session.add(pose)
    
    for pose_data in mala_postura_poses:
        # Check if pose already exists
        existing_pose = Posture.query.filter_by(name=pose_data["name"]).first()
        if existing_pose:
            existing_pose.therapy_types.append(TherapyType.query.get(mala_postura_id))
        else:
            pose = Posture(
                name=pose_data["name"],
                sanskrit_name=pose_data["sanskrit_name"],
                image_url=pose_data["image_url"],
                description=pose_data["description"],
                steps=pose_data["steps"],
                benefits=pose_data["benefits"],
                modifications=pose_data["modifications"]
            )
            pose.therapy_types.append(TherapyType.query.get(mala_postura_id))
            db.session.add(pose)
    
    db.session.commit()
    
    # Create directories for static files if they don't exist
    os.makedirs('static/images/poses', exist_ok=True)