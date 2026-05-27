import os, shutil, zipfile, json, random
from PIL import Image

for filename in os.listdir("packs"):
	file_path = os.path.join("packs", filename)
	if os.path.isfile(file_path) or os.path.islink(file_path):
		os.unlink(file_path)
	elif os.path.isdir(file_path):
		shutil.rmtree(file_path)

palettes = [
	"Acearo",
	"Agender",
	"Aromantic",
	"Asexual",
	"Bear",
	"Bigender",
	"Bisexual",
	"Demigender",
	"Demiromantic",
	"Demisexual",
	"Gay",
	"Genderfluid",
	"Genderqueer",
	"Intersex",
	"Lesbian",
	"Nonbinary",
	"Omnisexual",
	"Pansexual",
	"Philadelphia",
	"Polysexual",
	"Progress 2018",
	"Progress 2021",
	"Rainbow",
	"Transgender"
]


temp_icons_paths = []
def make_pack(version, *, use_old_icons_png = True, supported_formats = None, use_old_elytra_location = True):
	out_root = os.path.join("packs", str(version))
	os.makedirs(out_root, exist_ok=True)
	for palette in palettes:
		palette_root = os.path.join("assets", palette)
		pack_png = os.path.join(palette_root, "pack.png")
		elytra_png = os.path.join(palette_root, "elytra.png")
		xp_png = os.path.join(palette_root, "experience.png")
		zip_path = os.path.join(out_root, f"{palette} Pride Pack.zip")
		mcmeta = {
			"pack": {
				"pack_format": version,
				"description": f"Replaces XP bar and elytra\nastronomy487.com/pridepacks"
			}
		}
		if supported_formats is not None:
			mcmeta["pack"]["supported_formats"] = {
				"min_inclusive": supported_formats[0],
				"max_inclusive": supported_formats[1]
			}
			mcmeta["pack"]["min_format"] = supported_formats[0]
			mcmeta["pack"]["max_format"] = supported_formats[1]
		with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
			z.write(pack_png, "pack.png")
			z.writestr("pack.mcmeta", json.dumps(mcmeta, indent=2))
			if use_old_elytra_location:
				z.write(elytra_png, "assets/minecraft/textures/entity/elytra.png")
			else:
				z.write(elytra_png, "assets/minecraft/textures/entity/equipment/wings/elytra.png")
			if use_old_icons_png:
				temp_icons_path = f"temp_icons_{palette}.png"
				if not os.path.exists(temp_icons_path):
					base_icons_png = "icons.png"
					icons = Image.open(base_icons_png).convert("RGBA")
					xp = Image.open(xp_png).convert("RGBA")
					icons.paste(xp, (0, 69), xp)
					icons.save(temp_icons_path)
					temp_icons_paths.append(temp_icons_path)
				z.write(temp_icons_path, "assets/minecraft/textures/gui/icons.png")
			else:
				z.write(
					xp_png,
					"assets/minecraft/textures/gui/sprites/hud/experience_bar_progress.png"
				)

make_pack(1) # no elytra back then - just include it in the pack anyways
make_pack(2)
make_pack(3)
make_pack(4)
make_pack(5)
make_pack(6)
make_pack(7)
make_pack(8)
make_pack(9)
make_pack(12)
make_pack(13)
make_pack(15)

make_pack(34, use_old_icons_png = False, supported_formats = [18, 34])
make_pack(84, use_old_icons_png = False, supported_formats = [42, 84], use_old_elytra_location = False)

for temp_icons_path in temp_icons_paths:
	os.remove(temp_icons_path)