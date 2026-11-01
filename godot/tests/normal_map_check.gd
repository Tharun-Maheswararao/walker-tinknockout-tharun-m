## Curl check for tangent-space normal maps (Assignment 5 handout, Step 3),
## copied from the handout. Indentation is converted to tabs; the logic is
## unchanged. It is a helper, not a test: test_materials.gd and
## calibrate_normal_map.gd preload it.
##
## A real normal map encodes the slopes of a height surface, so its slope field
## is curl-free: the two mixed partial derivatives agree.

# ~0: slope field of a real surface in this convention.
# ~1: no surface behind it.
# ~2: real surface, other green convention.
static func curl_ratio(source: Image, directx := false, stride := 4) -> float:
	var img := source.duplicate() as Image
	if img.is_compressed():
		img.decompress()
	var s: float = -1.0 if directx else 1.0
	var curl_sq := 0.0
	var terms_sq := 0.0
	for v in range(1, img.get_height() - 1, stride):
		for u in range(1, img.get_width() - 1, stride):
			var t1 := (_dh_du(img, u, v + 1) - _dh_du(img, u, v - 1)) * 0.5
			var t2 := (_dh_dv(img, u + 1, v, s) - _dh_dv(img, u - 1, v, s)) * 0.5
			curl_sq += (t1 - t2) * (t1 - t2)
			terms_sq += t1 * t1 + t2 * t2
	return curl_sq / maxf(terms_sq, 1e-12)


static func _normal(img: Image, u: int, v: int) -> Vector3:
	var c := img.get_pixel(u, v)
	return Vector3(c.r, c.g, c.b) * 2.0 - Vector3.ONE


static func _dh_du(img: Image, u: int, v: int) -> float:
	var n := _normal(img, u, v)
	return -n.x / maxf(n.z, 0.05)


static func _dh_dv(img: Image, u: int, v: int, s: float) -> float:
	var n := _normal(img, u, v)
	return s * n.y / maxf(n.z, 0.05)
