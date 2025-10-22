import os
import random
import shutil

# Caminho base
base_dir = "dataset/silksong"
train_dir = os.path.join(base_dir, "train")
val_dir = os.path.join(base_dir, "val")

# Criar pasta de validação
os.makedirs(val_dir, exist_ok=True)

# Listar todas as imagens
images = [f for f in os.listdir(train_dir) if f.endswith(".jpg") or f.endswith(".png")]

# Separar 20% para validação
val_samples = random.sample(images, int(0.2 * len(images)))

for img in val_samples:
    label = img.rsplit(".", 1)[0] + ".txt"
    shutil.move(os.path.join(train_dir, img), os.path.join(val_dir, img))
    if os.path.exists(os.path.join(train_dir, label)):
        shutil.move(os.path.join(train_dir, label), os.path.join(val_dir, label))

print("Divisão concluída!")
