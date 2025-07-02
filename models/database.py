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
    
    # # Check if data already exists
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
         "steps": "Arrodillarse a cuatro patas.\n Manos alineadas con los hombros. \nLos dedos apuntan hacia delante. \nRodillas por debajo de las caderas. \nRedondear la espalda hacia arriba. \nMete el estómago. Dejar caer la cabeza. \nPausa arriba. Levanta las nalgas.\n Curvar la columna hacia abajo. \nVuelva al principio y repita.", 
         "benefits": "Ayuda a la espalda y los glúteos. Ejercicio de liberación muscular. Lubrica el giro.", 
         "modifications": "Levantar la pierna hacia un lado (perro haciendo pis)."},
        
        {"name": "Classical Fish", "sanskrit_name": "VMatsyasana", "image_url": "https://s3.ppllstatics.com/mujerhoy/www/multimedia/202206/21/media/cortadas/Matsyasana%20(1)-kN2D-U170491754246IBD-1248x1248@MujerHoy.jpeg", 
         "description": "Una postura rejuvenecedora que abre el pecho, estimula la garganta y mejora la respiración, mientras libera tensiones en la columna vertebral. Ideal para contrarrestar los efectos de estar sentado mucho tiempo.", 
         "steps": "Siéntese erguido. Extienda las piernas (postura del bastón). \nCon la ayuda de las manos, coloque el pie derecho sobre el muslo izquierdo y el pie izquierdo sobre el muslo derecho. \nFlexione la espalda sobre los codos hasta que la parte superior de la cabeza toque el suelo. \nSujete los dedos de los pies con las manos y arquee la espalda. \nSostener. Soltar.", 
         "benefits": "Estira muslos, rodillas y tobillos.", 
         "modifications": "No modificaciones necesarias."},
        
        {"name": "Prostration", "sanskrit_name": "Naman Pranamasana", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfPCJnVmUjpnwUIkBHGOPyjavxUXE98MU_yA-AEAeZrZIoPl_XFOrEe0gqkIVmfXZVf6g&usqp=CAU", 
         "description": "Una postura de reverencia profunda que combina flexión hacia adelante y ligera inversión, promoviendo humildad, calma mental y estiramiento suave de la columna vertebral.", 
         "steps": "Siéntese sobre las rodillas (Vajrasana).\n Sujete la parte inferior de las pantorrillas.\n Inclínese hacia delante. \nColoque la coronilla en el suelo, delante de las rodillas. \nLevante las nalgas hasta que los muslos estén verticales.\n Presione suavemente la barbilla contra el pecho. \nMantenga la posición.", 
         "benefits": "Activar el tronco. Preparación para pararse de cabeza y de hombros.", 
         "modifications": "Parada de cabeza."},
        
        {"name": "Aham Prema Mantra", "sanskrit_name": "Mantras", "image_url": "https://previews.123rf.com/images/inarik/inarik1503/inarik150300047/37386181-yoga-woman-in-meditation-sitting-in-lotus-pose-female-meditating-exercise-isolated-over-white.jpg", 
         "description": "Un poderoso mantra de origen sánscrito que significa 'Yo soy Amor Divino'. Su repetición consciente activa la vibración del amor puro, conectando el corazón con la conciencia universal. Ideal para meditación, sanación emocional y cultivo de compasión.", 
         "steps": "Siéntate cómodamente con la espalda recta, cierra los ojos, respira profundo y \n repite en silencio o en voz alta “Aham Prema” durante varios minutos con atención plena.", 
         "benefits": "Mejora de la concentración. Reducción del estrés. Autoconocimiento. Curación emocional. Refuerzo del sistema inmunitario. Aumento de los niveles de energía. Práctica espiritual más profunda.", 
         "modifications": "A) Siéntate sobre un cojín, una manta doblada o un bloque. \n B) Sentarse contra una pared.\n  C) Sentarse en una silla. \n D) Cambiar el cruce de las piernas. \n E) Siéntate en la postura del Héroe, del Perfecto o del Loto."},
        
        {"name": "Camel Wide Legs", "sanskrit_name": "Ustrasana", "image_url": "https://www.hola.com/horizon/landscape/777472627dce-ustrasana-t.jpg?im=Resize=(360),type=downsize", 
         "description": "Una poderosa flexión hacia atrás que abre el corazón y las caderas, combinando los beneficios de Ustrasana con un mayor estímulo para los músculos internos de los muslos y la pelvis. Ideal para contrarrestar el encorvamiento y mejorar la respiración profunda.", 
         "steps": "Arrodíllese con las piernas abiertas. \nApoye las manos en la parte posterior de la pelvis. \nSeñale con los dedos hacia abajo. \nInclínese hacia atrás. \nMentón cerca del esternón.\n Apoyar las palmas de las manos en los talones. \nLos pliegues de los codos miran hacia delante. \n Para salir, llevar una mano a la vez a las caderas. \nLevante la cabeza y el torso empujando los puntos de las caderas hacia abajo.", 
         "benefits": "Estira tobillos, muslos, ingles, abdominales, pecho, garganta, psoas.", 
         "modifications": "Las palmas contra las plantas."},
        
         {"name": "Forward Fold", "sanskrit_name": "Uttanasana", "image_url": "https://www.gaia.com/wp-content/uploads/standing-forward-fold-share.jpg", 
     "description": "Postura de flexión hacia adelante que alivia la tensión en la columna vertebral, cuello y hombros, promoviendo el flujo sanguíneo al cerebro.", 
     "steps": "De pie con pies separados al ancho de caderas.\nDobla las rodillas ligeramente.\nInclínate hacia adelante desde las caderas.\nDeja colgar la cabeza y relaja el cuello.\nColoca las manos en el suelo o agarra los codos opuestos.\nMantén la postura respirando profundamente.", 
     "benefits": "Alivia el estrés, calma la mente, estira isquiotibiales y espalda baja, mejora la circulación cerebral.", 
     "modifications": "Doblar más las rodillas o usar bloques bajo las manos."},
    
    {"name": "Legs Up the Wall", "sanskrit_name": "Viparita Karani", "image_url": "https://cdn.yogaeasy.de/production/uploads/article/picture/5853/large_legs-up-the-wall-pose.jpg", 
     "description": "Postura restaurativa que invierte el flujo sanguíneo, reduciendo la presión arterial y aliviando dolores de cabeza por tensión.", 
     "steps": "Siéntate cerca de una pared.\nGira el cuerpo y levanta las piernas apoyándolas en la pared.\nAcuéstate completamente con las nalgas tocando la pared.\nColoca los brazos a los lados con las palmas hacia arriba.\nCierra los ojos y respira profundamente por 5-10 minutos.", 
     "benefits": "Reduce el estrés, alivia piernas cansadas, mejora la circulación, calma el sistema nervioso.", 
     "modifications": "Colocar un cojín bajo las caderas o doblar ligeramente las rodillas."},
    
    {"name": "Seated Forward Bend", "sanskrit_name": "Paschimottanasana", "image_url": "https://www.arhantayoga.org/wp-content/uploads/2022/03/Seated-Forward-Bend-%E2%80%93-Paschimottanasana.jpg", 
     "description": "Flexión hacia adelante sentado que calma el sistema nervioso y alivia dolores de cabeza por estrés.", 
     "steps": "Siéntate con las piernas extendidas frente a ti.\nInhala y alarga la columna.\nExhala y dóblate hacia adelante desde las caderas.\nLlega a agarrar los pies o tobillos.\nRelaja la cabeza hacia las piernas.\nMantén la postura respirando profundamente.", 
     "benefits": "Calma la mente, reduce ansiedad, estira toda la espalda, estimula órganos abdominales.", 
     "modifications": "Usar una correa alrededor de los pies o doblar las rodillas."},
    
    {"name": "Bridge Pose", "sanskrit_name": "Setu Bandha Sarvangasana", "image_url": "https://cdn.yogajournal.com/wp-content/uploads/2021/11/YJ_Bridge-Pose_Andrew-Clark_2400x1350.png", 
     "description": "Postura suave de apertura del pecho que alivia la tensión en el cuello y hombros, común en dolores de cabeza tensionales.", 
     "steps": "Acuéstate boca arriba con rodillas dobladas y pies separados al ancho de caderas.\nColoca los brazos a los lados con las palmas hacia abajo.\nInhala y levanta las caderas hacia el techo.\nMantén los hombros relajados y el cuello largo.\nRespira profundamente y mantén la postura.", 
     "benefits": "Alivia el estrés, abre el pecho, fortalece la espalda, mejora la circulación.", 
     "modifications": "Colocar un bloque bajo las caderas para apoyo."},
    
    {"name": "Corpse Pose", "sanskrit_name": "Savasana", "image_url": "https://images.squarespace-cdn.com/content/v1/5d31ed671abe780001b2964d/1629138771884-ML3UZ97NYL33IQ3HJA7L/image-asset.jpeg", 
     "description": "Postura final de relajación que permite la integración completa de los beneficios de la práctica, calmando el sistema nervioso.", 
     "steps": "Acuéstate boca arriba con piernas extendidas y brazos a los lados.\nCierra los ojos y relaja completamente todo el cuerpo.\nRespira naturalmente y permite que el suelo te sostenga.\nPermanece en la postura por 5-15 minutos.", 
     "benefits": "Reduce el estrés y la ansiedad, disminuye la presión arterial, promueve la curación profunda.", 
     "modifications": "Colocar una manta bajo la cabeza o rodillas para mayor comodidad."},
    
    {"name": "Alternate Nostril Breathing", "sanskrit_name": "Nadi Shodhana Pranayama", "image_url": "https://www.ommagazine.com/wp-content/uploads/2022/02/ALTERNATE-NOSTRIL-BREATHING.jpg", 
     "description": "Técnica de respiración que equilibra los hemisferios cerebrales y alivia dolores de cabeza por tensión o desequilibrio energético.", 
     "steps": "Siéntate cómodamente con la espalda recta.\nColoca el pulgar derecho en la fosa nasal derecha y el anular en la izquierda.\nCierra la fosa nasal derecha e inhala por la izquierda.\nCierra ambas fosas nasales y retén brevemente.\nAbre la derecha y exhala completamente.\nInhala por la derecha, cierra y exhala por la izquierda.\nContinúa alternando por 5-10 rondas.", 
     "benefits": "Equilibra el sistema nervioso, calma la mente, mejora la concentración, alivia el estrés.", 
     "modifications": "Realizar sin retención si es incómodo."}
    ]
    
    insomnio_poses = [
        {"name": "Crocodile", "sanskrit_name": "Makarasana", "image_url": "https://images.ctfassets.net/p0sybd6jir6r/s9dGpWThHitnXPvqDrN5Q/e8fb4534d33ca3139176433156e2713a/Crocodile_Pose_1-4d14c71073ed4be3409dec347a112d6f.jpg?w=1600&fm=webp&q=70", 
         "description": "Una postura restaurativa que relaja profundamente el cuerpo, alivia la tensión en la espalda y favorece una respiración tranquila y consciente.", 
         "steps": "Relájese sobre el estómago.\n Brazos cruzados en el suelo por encima de la cabeza.\n Abrir las piernas.\n Girar los pies para que los talones apunten hacia dentro.\n Apretar los glúteos. \nPresione la pelvis contra el suelo. \nApoyar la frente en los brazos.", 
         "benefits": "Estira espalda, piernas y glúteos. Reduce el estrés. Mejora la postura.", 
         "modifications": "Coloque la frente en Yoni Mudra."},
        
        {"name": "Locust", "sanskrit_name": "Salabhasana", "image_url": "https://cdn.yogajournal.com/wp-content/uploads/2022/03/locust-pose_andrew-clark.jpg", 
         "description": "Un estiramiento completo que fortalece la espalda, activa los isquiotibiales y abre los hombros, mejorando la postura y la energía.", 
         "steps": "Túmbate boca abajo.\n Pies juntos. La frente en el suelo. \nColoque los brazos a los lados.\nLas palmas hacia arriba.\n Estire la barbilla ligeramente hacia delante. \nApoyar la barbilla en el suelo. Suavizar la parte delantera del cuerpo. \nLevante el pecho, las piernas y los brazos del suelo. \nExtienda las puntas de los dedos de las manos hacia los pies. \nMirar al frente.", 
         "benefits": "Tonifica los músculos de la espalda. Estimula la zona lumbar.", 
         "modifications": "1 pierna arriba. Piernas anchas. Manos debajo del cuerpo, a los lados o delante."},
        
        {"name": "Prostration", "sanskrit_name": "Naman Pranamasana", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfPCJnVmUjpnwUIkBHGOPyjavxUXE98MU_yA-AEAeZrZIoPl_XFOrEe0gqkIVmfXZVf6g&usqp=CAU", 
         "description": "Una postura de reverencia profunda que combina flexión hacia adelante y ligera inversión, promoviendo humildad, calma mental y estiramiento suave de la columna vertebral.", 
         "steps": "Siéntese sobre las rodillas (Vajrasana).\n Sujete la parte inferior de las pantorrillas.\n Inclínese hacia delante. \nColoque la coronilla en el suelo, delante de las rodillas. \nLevante las nalgas hasta que los muslos estén verticales.\n Presione suavemente la barbilla contra el pecho.\n Mantenga la posición.", 
         "benefits": "Activar el tronco. Preparación para pararse de cabeza y de hombros.", 
         "modifications": "Parada de cabeza."},
        
        {"name": "Child", "sanskrit_name": "Balasana", "image_url": "https://i.blogs.es/bdffc3/1366_2000-8-/1366_521.jpeg", 
         "description": "Una postura relajante que calma el cerebro y ayuda a aliviar el estrés y la ansiedad.", 
         "steps": "Póngase a cuatro patas. \nSiéntate sobre los talones y apoya la cabeza en la esterilla. \nColoca los brazos a los lados. \nCon cada exhalación relaja todo el cuerpo.", 
         "benefits": "Calma la mente, alivia el estrés y la fatiga, ayuda a aliviar los dolores de espalda y cuello.", 
         "modifications": "Aleje los dedos del cuerpo para estirar caderas, muslos y tobillos."},
        
        {"name": "Easy Ear To Shoulder I", "sanskrit_name": "Greeva Sanchalana", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5bNwoU3bXLK5ygb1AZIcPYRhMieq5m8tSx1bGXieqdrRvDgh6iZ1gZNszsgfg7WBK1Co&usqp=CAU", 
         "description": "Una postura suave que libera tensión en el cuello y mejora la movilidad cervical mediante estiramientos laterales conscientes.", 
         "steps": "Siéntate o ponte de pie. Cierre los ojos. \nMire directamente hacia delante.\n Relaje los hombros. \nMueva lentamente la cabeza hacia la derecha e intente tocar el hombro derecho con la oreja derecha (sin levantar los hombros). \nRepita en el otro lado.", 
         "benefits": "Flexibilidad en el cuello.", 
         "modifications": "A) Almohada bajo las nalgas. \nB) Espalda contra la pared. \nC) Palmas de las manos juntas en el centro del pecho. \nD) Dobla 1/4, 1/2 o 3/4 de la espalda hacia abajo. \nE) Entrelaza los dedos, extiende los brazos por encima de la cabeza, estírate hacia arriba y dóblate hacia delante."},
        
        {"name": "Bound Hand Headstand B", "sanskrit_name": "Baddha Hasta Sirsasana B", "image_url": "https://www.fitsri.com/wp-content/uploads/2021/01/bound-hands-headstand-1024x683.jpg", 
         "description": "Una postura invertida avanzada que fortalece el núcleo, mejora el equilibrio y revitaliza todo el cuerpo al estimular la circulación.", 
         "steps": "Siéntate sobre los talones. \nExtienda los brazos. \nDoble los codos y agarre el antebrazo opuesto por el codo. Coloque los antebrazos sobre la colchoneta y doble los dedos de los pies hacia abajo.\n Coloque la coronilla justo delante de los antebrazos. \nEmpiece a presionar los antebrazos firmemente contra la esterilla mientras baja los hombros para alargar el cuello. \nManteniendo la presión en los antebrazos y el cuello largo, levante las rodillas y lleve los pies hacia la cabeza. \nColoque la rodilla derecha sobre el tríceps derecho. \nColoque la rodilla izquierda sobre el tríceps izquierdo. \nLevante una pierna cada vez. \nContraiga el tronco.\n Sujetar. Los codos sostienen la mayor parte del peso. \nSi pierde el equilibrio, gire el cuerpo hacia delante. \nPara soltarse, ponga rápidamente las palmas de las manos en el suelo para mantener el equilibrio, \n doble la cintura y colóquese en plancha.", 
         "benefits": "El rey de las asanas. Piel brillante. Activa el núcleo.", 
         "modifications": "El rey de las asanas. Piel brillante. Parada de cabeza en Baddha Konasana, Parada de cabeza con piernas de águila. Parada de cabeza con piernas de loto. Parada de cabeza con Twisting Splits. Parada de cabeza con piernas anchas."},
        
        {"name": "Legs-Up-the-Wall", "sanskrit_name": "Viparita Karani", "image_url": "https://cdn.yogaeasy.de/production/uploads/article/picture/5853/large_legs-up-the-wall-pose.jpg",
     "description": "Postura restaurativa que activa el sistema parasimpático, reduciendo el estrés y preparando el cuerpo para el sueño profundo.",
     "steps": "Siéntate cerca de una pared.\nAcuéstate de espaldas y estira las piernas verticalmente contra la pared.\nColoca los brazos a los lados con las palmas hacia arriba.\nCierra los ojos y respira profundamente durante 5-10 minutos.",
     "benefits": "Reduce la ansiedad, alivia piernas cansadas, calma el sistema nervioso central.",
     "modifications": "Coloca un cojín bajo la pelvis para mayor comodidad."},

    {"name": "Reclining Butterfly", "sanskrit_name": "Supta Baddha Konasana", "image_url": "https://www.fitsri.com/wp-content/uploads/2020/07/Supta-Baddha-konasana.jpg",
     "description": "Apertura suave de caderas que libera tensiones emocionales acumuladas en la pelvis, zona donde se almacena mucho estrés.",
     "steps": "Acuéstate boca arriba.\nUne las plantas de los pies y deja caer las rodillas hacia los lados.\nColoca las manos sobre el abdomen o estiradas a los lados.\nMantén la postura 3-5 minutos con respiración abdominal.",
     "benefits": "Estimula órganos reproductores, alivia molestias menstruales, reduce fatiga.",
     "modifications": "Apoya las rodillas con cojines si hay tensión en las ingles."},

    {"name": "Corpse Pose with Bolster", "sanskrit_name": "Savasana", "image_url": "https://www.fitsri.com/wp-content/uploads/2022/03/corpse-pose-with-bolster-1024x683.jpg",
     "description": "Variación de la postura final de relajación que profundiza la conexión mente-cuerpo mediante soporte físico.",
     "steps": "Coloca un bolster longitudinal bajo las rodillas.\nAcuéstate boca arriba con piernas extendidas.\nColoca una manta doblada bajo la cabeza.\nCubre tus ojos con un antifaz o paño suave.\nPermanece 10-15 minutos.",
     "benefits": "Disminuye la presión arterial, sincroniza ondas cerebrales theta, induce relajación profunda.",
     "modifications": "Usa mantas adicionales para mayor calidez y confort."},

    {"name": "Seated Forward Bend", "sanskrit_name": "Paschimottanasana", "image_url": "https://www.arhantayoga.org/wp-content/uploads/2022/03/Seated-Forward-Bend-%E2%80%93-Paschimottanasana.jpg",
     "description": "Flexión hacia adelante que masajea órganos abdominales y activa el nervio vago, clave para la relajación.",
     "steps": "Siéntate con piernas extendidas.\nInhala alargando la columna.\nExhala doblando desde las caderas.\nAgarra tobillos o pies.\nRelaja cabeza y cuello.\nMantén 1-3 minutos.",
     "benefits": "Calma la mente, estimula el hígado y riñones, alivia dolores de cabeza.",
     "modifications": "Dobla las rodillas o usa una correa alrededor de los pies."},

    {"name": "4-7-8 Breathing", "sanskrit_name": "Pranayama", "image_url": "https://miro.medium.com/v2/resize:fit:1024/1*k9ceMn89seNhCGqGzHtouw.jpeg",
     "description": "Técnica respiratoria basada en la ciencia que activa la respuesta de relajación en minutos.",
     "steps": "Siéntate con espalda recta.\nInhala por nariz contando 4.\nRetén el aire contando 7.\nExhala por boca contando 8.\nRepite 4-8 ciclos.",
     "benefits": "Reduce ritmo cardíaco, oxigena sangre, calma mente hiperactiva.",
     "modifications": "Acostado boca arriba con manos sobre abdomen."},

    {"name": "Sleeping Swan", "sanskrit_name": "Eka Pada Rajakapotasana", "image_url": "https://www.arhantayoga.org/es/wp-content/uploads/2023/02/Sleeping-Swan-Pose-Yin-1.jpg",
     "description": "Apertura profunda de caderas que libera emociones reprimidas y tensiones físicas.",
     "steps": "Desde cuadrupedia, lleva rodilla derecha hacia mano derecha.\nExtiende pierna izquierda atrás.\nBaja torso sobre bolster o almohada.\nMantén 2-3 minutos por lado.",
     "benefits": "Libera tensión pélvica, estimula órganos digestivos, alivia ciática.",
     "modifications": "Usa soportes bajo cadera y cabeza."}
    ]
    
    mala_postura_poses = [
        {"name": "Child", "sanskrit_name": "Balasana", "image_url": "https://i.blogs.es/bdffc3/1366_2000-8-/1366_521.jpeg", 
         "description": "Una postura relajante que calma el cerebro y ayuda a aliviar el estrés y la ansiedad.", 
         "steps": "Póngase a cuatro patas.\n Siéntate sobre los talones y apoya la cabeza en la esterilla.\n Coloca los brazos a los lados.\n Con cada exhalación relaja todo el cuerpo.", 
         "benefits": "Calma la mente, alivia el estrés y la fatiga, ayuda a aliviar los dolores de espalda y cuello.", 
         "modifications": "Aleje los dedos del cuerpo para estirar caderas, muslos y tobillos."},
        
        {"name": "Cat", "sanskrit_name": "Matwork", "image_url": "https://kavaalya.com/wp-content/uploads/2023/10/postura-gato-marjaryasana.jpg", 
         "description": "Un movimiento fluido y terapéutico que mejora la flexibilidad de la columna vertebral, libera tensiones y masajea los órganos abdominales.", 
         "steps": "Arrodillarse a cuatro patas. \nManos alineadas con los hombros. \nLos dedos apuntan hacia delante. \nRodillas por debajo de las caderas. \nRedondear la espalda hacia arriba. \nMete el estómago. Dejar caer la cabeza. \nPausa arriba. Levanta las nalgas.\n Curvar la columna hacia abajo. \nVuelva al principio y repita.", 
         "benefits": "Ayuda a la espalda y los glúteos. Ejercicio de liberación muscular. Lubrica el giro.", 
         "modifications": "Levantar la pierna hacia un lado (perro haciendo pis)."},
        
        {"name": "Abdominal Stretch", "sanskrit_name": "Udarakarshanasana", "image_url": "https://pranayoga.co.in/asana/wp-content/uploads/Udarakarshanasana%E2%80%93Abdominal-Stretch-Posture.jpg", 
         "description": "Una torsión en cuclillas que estimula la digestión, desintoxica el cuerpo y mejora la movilidad de la parte inferior del tronco.", 
         "steps": "Empezar en cuclillas estrechas (talones levantados si es necesario). \nColoque las palmas de las manos delante de las rodillas. En la espiración, llevar la rodilla derecha al suelo a través de la línea media (hacia el pie izquierdo). \nGire el cuerpo hacia la izquierda. Mire hacia atrás.\n La rodilla izquierda permanece lo más quieta posible.\n Vuelva al centro. Repita del otro lado.", 
         "benefits": "Mejora la flexibilidad de caderas, rodillas y tobillos. Desintoxicación.", 
         "modifications": "Mientras caminas hacia delante, lleva la rodilla opuesta hacia o sobre el suelo."},
        
        {"name": "Alice In Wonderland", "sanskrit_name": "Tadasana", "image_url": "https://www.yogabasics.com/yogabasics2017/wp-content/uploads/2013/11/Tadasana_2280.jpg", 
         "description": "Una postura de pie fundamental que mejora el equilibrio, alinea la postura y activa todo el cuerpo con serenidad y firmeza.", 
         "steps": "Imagina que tienes una poción mágica que te dio Alicia en el País de las Maravillas.\n Bebe. ¡Vaya! Cada vez eres más alto (estira las manos sobre la cabeza).", 
         "benefits": "Equilibrio. Calmante. Mejora la postura. Fortalece las piernas. Refuerza el tronco.", 
         "modifications": "Manos en oración detrás de la espalda. Ojos cerrados."},
        
        {"name": "Base", "sanskrit_name": "Prarambhik Sthiti", "image_url": "https://wiki.yoga-vidya.de/images/thumb/f/ff/Grundhaltung_Prarambhik_Sthiti_bzw-_Parambhasana_-_Langsitz_-_Ausgangslage.jpg/250px-Grundhaltung_Prarambhik_Sthiti_bzw-_Parambhasana_-_Langsitz_-_Ausgangslage.jpg", 
         "description": "Una postura de descanso que calma la mente, alinea la columna y reduce el estrés al mantener el torso erguido y relajado.", 
         "steps": "Siéntate con las piernas extendidas. \nPies juntos. \nPalmas detrás de las nalgas. Dedos hacia atrás. \nLos brazos sostienen el 20% del peso del torso.\n El otro 80% del peso del torso lo soportan la espalda y los músculos centrales (siente cómo la columna se hace más alta). \nMira al frente (o cierra los ojos).", 
         "benefits": "Fortalece los músculos de la espalda. Estira los hombros y el pecho.", 
         "modifications": "Siéntese sobre una manta doblada para levantar la pelvis. Espalda contra la pared."},
        
        {"name": "Crocodile", "sanskrit_name": "Makarasana", "image_url": "https://images.ctfassets.net/p0sybd6jir6r/s9dGpWThHitnXPvqDrN5Q/e8fb4534d33ca3139176433156e2713a/Crocodile_Pose_1-4d14c71073ed4be3409dec347a112d6f.jpg?w=1600&fm=webp&q=70", 
         "description": "Una postura restaurativa que relaja profundamente el cuerpo, alivia la tensión en la espalda y favorece una respiración tranquila y consciente.", 
         "steps": "Relájese sobre el estómago.\n Brazos cruzados en el suelo por encima de la cabeza.\n Abrir las piernas. \nGirar los pies para que los talones apunten hacia dentro.\n Apretar los glúteos. \nPresione la pelvis contra el suelo.\n Apoyar la frente en los brazos.", 
         "benefits": "Estira espalda, piernas y glúteos. Reduce el estrés. Mejora la postura.", 
         "modifications": "Coloque la frente en Yoni Mudra."},
        
         {"name": "Mountain Pose", "sanskrit_name": "Tadasana", "image_url": "https://www.verywellfit.com/thmb/Cq397HlPq6j9j1aPOZGaXrGvyKE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/mountainpose-5c536e174cedfd0001efd515.jpg",
     "description": "Postura fundamental que enseña la alineación corporal correcta desde los pies hasta la cabeza.",
     "steps": "De pie con pies juntos o separados al ancho de caderas.\nDistribuye el peso uniformemente en ambos pies.\nEngancha los músculos del muslo y levanta las rótulas.\nAlarga la columna, abre el pecho y relaja los hombros.\nMantén la barbilla paralela al suelo.",
     "benefits": "Mejora la postura, aumenta la conciencia corporal, fortalece muslos y rodillas.",
     "modifications": "Pararse contra una pared para verificar la alineación."},

    {"name": "Cobra Pose", "sanskrit_name": "Bhujangasana", "image_url": "https://rishikeshashtangayogaschool.com/blog/wp-content/uploads/2021/11/cobra-pose_11zon.jpg",
     "description": "Flexión hacia atrás suave que fortalece los músculos de la espalda y contrarresta el encorvamiento.",
     "steps": "Acuéstate boca abajo con manos bajo los hombros.\nInhala y levanta el pecho manteniendo las caderas en el suelo.\nMantén los codos ligeramente doblados y los hombros alejados de las orejas.\nSostén por 15-30 segundos.",
     "benefits": "Fortalece la columna vertebral, abre el pecho, estira abdominales.",
     "modifications": "Realizar con los antebrazos en el suelo para una versión más suave."},

    {"name": "Thread the Needle", "sanskrit_name": "Parsva Balasana", "image_url": "https://www.theyogacollective.com/wp-content/uploads/2019/11/Thread-the-Needle-Pose-for-Pose-Pge-1200x800.jpeg",
     "description": "Torsión que libera tensión en hombros y columna torácica, áreas clave en problemas posturales.",
     "steps": "Comienza a cuatro patas.\nDesliza el brazo derecho por debajo del izquierdo, bajando el hombro y la mejilla al suelo.\nExtiende el brazo izquierdo hacia adelante.\nMantén 30 segundos y repite en el otro lado.",
     "benefits": "Libera tensión en hombros, mejora movilidad torácica, alivia dolor de cuello.",
     "modifications": "Colocar una almohada bajo la cabeza si no llega al suelo."},

    {"name": "Bridge Pose", "sanskrit_name": "Setu Bandhasana", "image_url": "https://cdn.yogajournal.com/wp-content/uploads/2021/11/YJ_Bridge-Pose_Andrew-Clark_2400x1350.png",
     "description": "Fortalece los músculos posteriores de la espalda y glúteos, contrarrestando el efecto de estar sentado.",
     "steps": "Acostado boca arriba con rodillas dobladas y pies separados al ancho de caderas.\nLevanta las caderas manteniendo hombros y cabeza en el suelo.\nEntrelaza las manos bajo la espalda y presiona los brazos contra el suelo.\nMantén 30 segundos.",
     "benefits": "Fortalece espalda baja y glúteos, abre el pecho, estimula la tiroides.",
     "modifications": "Colocar un bloque bajo las caderas para soporte."},

    {"name": "Wall Angels", "sanskrit_name": "Kapota Pratikriyasana", "image_url": "https://cdn.betterme.world/articles/wp-content/uploads/2025/01/ready-4-5.png",
     "description": "Ejercicio postural que corrige la posición de los hombros y abre el pecho.",
     "steps": "Párate contra una pared con pies a 15 cm de distancia.\nPresiona espalda baja, omóplatos y cabeza contra la pared.\nLevanta los brazos en posición de 'W' y deslízalos lentamente hacia arriba hasta formar una 'Y'.\nRepite 10 veces.",
     "benefits": "Corrige hombros redondeados, mejora movilidad escapular, aumenta conciencia postural.",
     "modifications": "Usar una banda de resistencia para mayor desafío."},

    {"name": "Scapular Squeeze", "sanskrit_name": "Skandha Chalanasana", "image_url": "https://images.ctfassets.net/hjcv6wdwxsdz/mVHB0PhK72zwAIUZS0Q2W/f360363b46b9fd93f1e25061bd7a99a0/woman-doing-scapular-clocks-exercises.png",
     "description": "Ejercicio para fortalecer los músculos romboides que sostienen la escápula.",
     "steps": "Sentado o de pie con brazos a los lados.\nJunta los omóplatos como si sostuvieras una pelota entre ellos.\nMantén 5 segundos y relaja.\nRepite 10-15 veces.",
     "benefits": "Fortalece músculos posturales superiores, mejora posición de los hombros, previene dolor cervical.",
     "modifications": "Usar una banda de resistencia alrededor de las manos para mayor intensidad."}
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