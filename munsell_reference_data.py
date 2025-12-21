"""
Munsell Color Reference Data
Data provided by Professor Marcelo Claro
Format: H V C R G B
H = Hue (e.g., 7.5PB, 10PB, 2.5P)
V = Value (lightness, 0-10)
C = Chroma (saturation)
R, G, B = Red, Green, Blue values
"""

MUNSELL_REFERENCE_DATA = [
    # Hue, Value, Chroma, R, G, B
    ("7.5PB", 0.2, 2, 5.063823211513849, 5.163155553572306, 29.706817501842973),
    ("7.5PB", 0.2, 4, 4.52741091827587, 2.5404209580620676, 39.91740416590666),
    ("10PB", 0.2, 2, 13.280168863015449, 2.680877989857141, 29.47964154643309),
    ("2.5P", 0.2, 2, 17.168258126754388, 1.3437546750566913, 28.67530312759932),
    ("5P", 0.2, 2, 20.54994784047107, 0.016021946274414237, 27.635271408748096),
    ("5GY", 0.4, 2, 8.498686364563637, 17.294415043727756, 0.9536445704568177),
    ("7.5GY", 0.4, 2, 5.344331179473867, 17.700429452217744, 4.36651046816763),
    ("10GY", 0.4, 2, 2.5924662347298817, 18.034583399104978, 7.554415504520902),
    ("2.5G", 0.4, 2, 0.9742800933702187, 18.214135164893094, 9.648362058087944),
    ("2.5PB", 0.4, 2, 0.6501591879428638, 15.509941311505836, 32.42084354094579),
    ("5PB", 0.4, 2, 5.029972228570205, 14.357544485089248, 33.173037298042665),
    ("7.5PB", 0.4, 2, 11.642193776759667, 12.578590500467165, 33.77775958384256),
    ("7.5PB", 0.4, 4, 9.978082024375382, 10.173812841849234, 43.98921451410903),
    ("7.5PB", 0.4, 6, 9.246531070800009, 6.306308130600004, 54.4342913956687),
    ("7.5PB", 0.4, 8, 9.31455242280002, 1.4645554932666658, 64.43197271179059),
    ("10PB", 0.4, 2, 17.514228194996143, 10.557034142733796, 33.69635700931716),
    ("10PB", 0.4, 4, 20.21248825370552, 6.632810620199998, 42.67839454885113),
    ("10PB", 0.4, 6, 23.563961853273575, 1.6501558910640104, 51.37089530931042),
    ("2.5P", 0.4, 2, 21.0920500481392, 9.08174033279661, 32.933337327455014),
    ("2.5P", 0.4, 4, 25.181995418216058, 4.44784586537015, 41.196021871568206),
    ("5P", 0.4, 2, 24.314891717864665, 7.728413558221978, 31.423459870304853),
    ("5P", 0.4, 4, 29.590096502535978, 2.2080381028782647, 39.40667686160667),
    ("7.5P", 0.4, 2, 26.27784728645523, 6.800274461471352, 30.46074708646904),
    ("7.5P", 0.4, 4, 31.796583665032546, 1.079713504436624, 37.97077393605867),
    ("10P", 0.4, 2, 27.64608165615076, 6.18435984833968, 29.430396024810953),
    ("10P", 0.4, 4, 33.45075093047909, 0.22617099540000052, 36.634974150568034),
    ("2.5RP", 0.4, 2, 28.634995373822207, 5.755071686869429, 28.481574637545844),
    ("5RP", 0.4, 2, 30.052694667428067, 5.104438064541705, 27.058019),
]


def get_munsell_notation(hue, value, chroma):
    """
    Format Munsell notation from components.
    
    Args:
        hue (str): Munsell hue (e.g., '7.5PB', '10PB')
        value (float): Munsell value (lightness)
        chroma (float or int): Munsell chroma (saturation)
    
    Returns:
        str: Formatted Munsell notation (e.g., '7.5PB 0.2/2')
    """
    return f"{hue} {value}/{chroma}"


def rgb_to_munsell_nearest(r, g, b):
    """
    Convert RGB values to Munsell notation using nearest neighbor search
    in the reference data.
    
    Args:
        r (float): Red value (0-255)
        g (float): Green value (0-255)
        b (float): Blue value (0-255)
    
    Returns:
        tuple: (munsell_notation, distance, reference_rgb)
            - munsell_notation (str): Closest Munsell notation
            - distance (float): Euclidean distance to the closest match
            - reference_rgb (tuple): RGB values of the closest reference color
    """
    import numpy as np
    
    # Normalize input RGB to match reference data scale if needed
    input_rgb = np.array([r, g, b])
    
    min_distance = float('inf')
    closest_munsell = None
    closest_rgb = None
    
    for hue, value, chroma, ref_r, ref_g, ref_b in MUNSELL_REFERENCE_DATA:
        ref_rgb = np.array([ref_r, ref_g, ref_b])
        
        # Calculate Euclidean distance
        distance = np.linalg.norm(input_rgb - ref_rgb)
        
        if distance < min_distance:
            min_distance = distance
            closest_munsell = get_munsell_notation(hue, value, chroma)
            closest_rgb = (ref_r, ref_g, ref_b)
    
    return closest_munsell, min_distance, closest_rgb


def rgb_to_munsell_deltaE(r, g, b):
    """
    Convert RGB values to Munsell notation using Delta E color difference
    (perceptually uniform color distance).
    
    Args:
        r (float): Red value (0-255)
        g (float): Green value (0-255)
        b (float): Blue value (0-255)
    
    Returns:
        tuple: (munsell_notation, delta_e, reference_rgb)
            - munsell_notation (str): Closest Munsell notation
            - delta_e (float): Delta E 2000 color difference
            - reference_rgb (tuple): RGB values of the closest reference color
    """
    try:
        from skimage.color import rgb2lab, deltaE_ciede2000
        import numpy as np
        
        # Normalize RGB to 0-1 range for skimage
        input_rgb_normalized = np.array([[[r/255, g/255, b/255]]])
        input_lab = rgb2lab(input_rgb_normalized)
        
        min_delta_e = float('inf')
        closest_munsell = None
        closest_rgb = None
        
        for hue, value, chroma, ref_r, ref_g, ref_b in MUNSELL_REFERENCE_DATA:
            # Normalize reference RGB to 0-1 range
            ref_rgb_normalized = np.array([[[ref_r/255, ref_g/255, ref_b/255]]])
            ref_lab = rgb2lab(ref_rgb_normalized)
            
            # Calculate Delta E 2000
            delta_e = deltaE_ciede2000(input_lab, ref_lab)[0][0]
            
            if delta_e < min_delta_e:
                min_delta_e = delta_e
                closest_munsell = get_munsell_notation(hue, value, chroma)
                closest_rgb = (ref_r, ref_g, ref_b)
        
        return closest_munsell, min_delta_e, closest_rgb
    
    except ImportError:
        # Fallback to Euclidean distance if skimage is not available
        return rgb_to_munsell_nearest(r, g, b)


# Legacy function name for backward compatibility
def rgb_to_embrapa_munsell(r, g, b):
    """
    Convert RGB to Munsell notation.
    This is the main function that should be used.
    Uses Delta E method if available, otherwise Euclidean distance.
    
    Args:
        r (float): Red value (0-255)
        g (float): Green value (0-255)
        b (float): Blue value (0-255)
    
    Returns:
        str: Munsell notation (e.g., '7.5PB 0.2/2')
    """
    munsell_notation, _, _ = rgb_to_munsell_deltaE(r, g, b)
    return munsell_notation


if __name__ == "__main__":
    # Test the functions
    print("Testing RGB to Munsell conversion:")
    print("=" * 60)
    
    # Test with a sample RGB value
    test_rgb = (10, 15, 30)
    print(f"\nTest RGB: {test_rgb}")
    
    # Using Euclidean distance
    munsell_euclidean, dist, ref_rgb = rgb_to_munsell_nearest(*test_rgb)
    print(f"\nEuclidean Distance Method:")
    print(f"  Closest Munsell: {munsell_euclidean}")
    print(f"  Distance: {dist:.2f}")
    print(f"  Reference RGB: ({ref_rgb[0]:.2f}, {ref_rgb[1]:.2f}, {ref_rgb[2]:.2f})")
    
    # Using Delta E
    munsell_deltae, delta_e, ref_rgb_de = rgb_to_munsell_deltaE(*test_rgb)
    print(f"\nDelta E Method:")
    print(f"  Closest Munsell: {munsell_deltae}")
    print(f"  Delta E: {delta_e:.2f}")
    print(f"  Reference RGB: ({ref_rgb_de[0]:.2f}, {ref_rgb_de[1]:.2f}, {ref_rgb_de[2]:.2f})")
    
    print("\n" + "=" * 60)
    print(f"Total reference colors: {len(MUNSELL_REFERENCE_DATA)}")
