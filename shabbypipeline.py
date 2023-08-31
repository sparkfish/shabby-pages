from augraphy import *
import os
import random
import cv2


def get_pipeline():

    ################################################################################
    # CONTROLLING VARIATION
    #
    # We can control the outputs of the pipeline by setting values here.
    ################################################################################

    # BadPhotoCopy.mask is a mask of noise to generate the effect with
    badphotocopy_noise_mask = None
    # BadPhotoCopy.noise_type determines which mask pattern to use
    badphotocopy_noise_type = -1
    # BadPhotoCopy.noise_side determines where to add noise
    badphotocopy_noise_side = "random"
    # BadPhotoCopy.noise_iteration determines how many times to apply noise in the mask
    badphotocopy_noise_iteration = (1, 2)
    # BadPhotoCopy.noise_size determines the scale of noise in the mask
    badphotocopy_noise_size = (1, 2)
    # BadPhotoCopy.noise_value determines the intensity of the noise
    badphotocopy_noise_value = (128, 196)
    # BadPhotoCopy.noise_sparsity determines the sparseness of noise
    badphotocopy_noise_sparsity = (0.3, 0.6)
    # BadPhotoCopy.noise_concentration determines the concentration of noise
    badphotocopy_noise_concentration = (0.1, 0.5)
    # BadPhotoCopy.blur_noise determines whether or or not to add blur
    badphotocopy_blur_noise = random.choice([0, 1])
    # BadPhotoCopy.blur_noise_kernel gives the dimensions for the noise kernel
    badphotocopy_blur_noise_kernel = random.choice([(3, 3), (5, 5)])
    # BadPhotoCopy.wave_pattern enables the wave pattern in the noise mask
    badphotocopy_wave_pattern = random.choice([0, 1])
    # BadPhotoCopy.edge_effect adds the Sobel edge effect to the noise mask
    badphotocopy_edge_effect = random.choice([0, 1])
    # BadPhotoCopy.p is the probability to run this augmentation
    badphotocopy_p = (random.random() > 0.5) * 1

    # BindingsAndFasteners.overlay_types can be min, max, or mix
    bindingsandfasteners_overlay_types = "darken"
    # BindingsAndFasteners.foreground is the path to fg image or the image itself
    bindingsandfasteners_foreground = None
    # BindingsAndFasteners.effect_type is "punch_holes", "binding_holes", or "clips"
    bindingsandfasteners_effect_type = random.choice(["punch_holes", "binding_holes", "clips"])
    # BindingsAndFasteners.ntimes gives how many fg images to draw
    bindingsandfasteners_ntimes = (10, 20) if bindingsandfasteners_effect_type == "binding_holes" else (2, 3)
    # BindingsAndFasteners.nscales is the scale of the fg image size
    bindingsandfasteners_nscales = (0.9, 1)
    # BindingsAndFasteners.edge gives the edge to place the images on
    bindingsandfasteners_edge = "random"
    # BindingsAndFasteners.edge_offset is how far from the page edge to draw
    bindingsandfasteners_edge_offset = (10, 50)

    # BleedThrough.intensity_range is a tuple with bounds for bleed intensity to be selected from
    bleedthrough_intensity_range = (0.1, 0.2)
    # BleedThrough.color_range is a tuple with bounds for color noise
    bleedthrough_color_range = (32, 224)
    # BleedThrough.ksize is a tuple of height/width pairs for sampling kernel size
    bleedthrough_ksize = (17, 17)
    # BleedThrough.sigmaX is the standard deviation of the kernel along the x-axis
    bleedthrough_sigmaX = 0
    # BleedThrough.alpha is the intensity of the bleeding effect, recommended 0.1-0.5
    bleedthrough_alpha = random.uniform(0.05, 0.1)
    # BleedThrough.offsets is a pair of x and y distances to shift the bleed with
    bleedthrough_offsets = (10, 20)

    # Brightness.range is a pair of floats determining the brightness delta
    brightness_range = (0.9, 1.1)
    # Brightness.min_brightness is a flag to enable min brightness intensity value in the augmented image
    brightness_min_brightness = 0
    # Brightness.min_brightness_value is a pair of ints determining the minimum brightness intensity of augmented image
    brightness_min_brightness_value = (120, 150)

    # BrightnessTexturize.range determines the value range of samples for the brightness matrix
    brightnesstexturize_range = (0.9, 0.99)
    # BrightnessTexturize.deviation is additional variation for the uniform sample
    brightnesstexturize_deviation = 0.03

    # ColorPaper.hue_range is range of randomized hue value
    colorpaper_hue_range = (0, 255)
    # ColorPaper.saturation_range is range randomized of saturation value
    colorpaper_saturation_range = (10, 40)

    # ColorShift.color_shift_offset_x_range is a pair of ints/floats determining the value of x offset in shifting each color channel
    color_shift_offset_x_range=(1, 2)
    # ColorShift.color_shift_offset_y_range is a pair of ints/floats determining the value of y offset in shifting each color channel
    color_shift_offset_y_range=(1, 2)
    # ColorShift.color_shift_iterations is a pair of ints determining the number of iterations in applying the color shift operation
    color_shift_iterations=(1, 2)
    # ColorShift.color_shift_brightness_range is a pair of floats determining the brightness value of the shifted color channel
    color_shift_brightness_range=(0.9, 1.1)
    # ColorShift.color_shift_gaussian_kernel_range is a pair of ints determining the Gaussian kernel value in blurring the shifted image
    color_shift_gaussian_kernel_range=(1, 1)

    # DelaunayTessellation.n_points_range is a tuple of ints determining the triangulating points of the effect
    delaunay_tessellation_n_points_range=(500, 800)
    # DelaunayTessellation.n_horizontal_points_range is a tuple of ints determining the number of points in horizontal edge
    delaunay_tessellation_n_horizontal_points_range=(500, 800)
    # DelaunayTessellation.n_vertical_points_range is a tuple of ints determining the number of points in vertical edge
    delaunay_tessellation_n_vertical_points_range=(500, 800)
    # DelaunayTessellation.noise_type is the types of noise in the effect.
    delaunay_tessellation_noise_type="random"

    # DirtyDrum.line_width_range determines the range from which drum line widths are sampled
    dirtydrum_line_width_range = (1, 6)
    # concentration of dirty drum line
    dirtydrum_line_concentration = random.uniform(0.05, 0.15)
    # DirtyDrum.direction is 0 for horizontal, 1 for vertical, 2 for both
    dirtydrum_direction = random.randint(0, 2)
    # DirtyDrum.noise_intensity changes how significant the effect is, recommended 0.8-1.0
    dirtydrum_noise_intensity = random.uniform(0.6, 0.95)
    # DirtyDrum.noise_value determine the intensity of dirty drum noise
    dirtydrum_noise_value = (128, 224)
    # DirtyDrum.ksize is a tuple of height/width pairs from which to sample kernel size
    dirtydrum_ksize = random.choice([(3, 3), (5, 5), (7, 7)])
    # DirtyDrum.sigmaX is the stdev of the kernel in the x direction
    dirtydrum_sigmaX = 0
    # DirtyDrum.p is the probability to run this augmentation
    dirtydrum_p = (random.random() > 0.5) * 1

    # DirtyRollers.line_width_range determines the width of roller lines
    dirtyrollers_line_width_range = (2, 32)
    # DirtyRollers.scanline_type changes the background of lines
    dirtyrollers_scanline_type = 0
    # DirtyRollers.p is the probability to run this augmentation
    dirtyrollers_p = (random.random() > 0.5) * 1

    # Dithering.dither_type can be 'ordered' for ordered dithering or another string for floyd-steinberg dithering
    dithering_dither_type = random.choice(["ordered", "floyd-steinberg"])
    # Dithering.order is a pair of ints determining the range of order number for ordered dithering
    dithering_order = (2, 5)
    # dithering.p is the probability to run this augmentation
    dithering_p = (random.random() > 0.7) * 1

    # Faxify.scale_range is a pair of ints determining the scaling magnitude
    faxify_scale_range = (0.2, 0.4)
    # Faxify.monochrome determines whether the image will get the halftone effect
    faxify_monochrome = random.choice([0, 1])
    # Faxify.monochrome_method is the binarization method for applying the effect
    faxify_monochrome_method = "random"
    # Faxify.monochrome_argument is the input arguments to the monochrome method
    faxify_monochrome_arguments = {}
    # Faxify.monochrome_threshold is the simple binarization threshold value
    faxify_halftone = random.choice((0, 1))
    # Faxify.invert determines whether to invert the grayscale value in halftone
    faxify_invert = 1
    # Faxify.half_kernel_size is half the Gaussian kernel size for halftone
    faxify_half_kernel_size = (1, 1)
    # Faxify.angle is the angle of the halftone effect
    faxify_angle = (0, 360)
    # Faxify.sigma is the sigma value of the Gaussian kernel in the halftone effect
    faxify_sigma = (1, 3)

    # Gamma.range is an interval from which to sample a gamma shift
    gamma_range = (0.8, 1.2)

    # Geometric.scale is a pair determining how to scale the image
    geometric_scale = (1, 1)
    # Geometric.translation is a pair determining where to translate the image
    geometric_translation = (0, 0)
    # Geometric.fliplr flips the image left and right
    geometric_fliplr = 0
    # Geometric.flipud flips the image up and down
    geometric_flipud = 0
    # Geometric.crop is a tuple of four points giving the corners of a crop region
    geometric_crop = []
    # Geometric.rotate_range is a pair determining the rotation angle sample range
    geometric_rotate_range = (0, 0)
    # Geometric.randomize determines whether to randomize geometric transformation
    geometric_randomize = 0

    # InkBleed.intensity_range is a tuple with bounds for bleed intensity to be selected from
    inkbleed_intensity_range = (0.5, 0.7)
    # InkBleed.kernel_size determines the radius of the bleed effect
    inkbleed_kernel_size = random.choice([(5, 5), (3, 3)])
    # InkBleed.severity determines significance of bleed effect
    inkbleed_severity = (0.2, 0.4)
    # InkBleed.p is the probability to run this augmentation
    inkbleed_p = 0.5
    
    # InkColorSwap.ink_swap_color is the swapping color (BGR) of the effect
    ink_swap_color=(25,25,25)
    # InkColorSwap.ink_swap_sequence_number_range is a pair of ints determing the consecutive swapping number in the detected contours
    ink_swap_sequence_number_range=(5, 10)
    # InkColorSwap.ink_swap_min_width_range is a pair of ints/floats determining the minimum width of the contour
    ink_swap_min_width_range=(2, 3)
    # InkColorSwap.ink_swap_max_width_range is a pair of ints/floats determining the maximum width of the contour
    ink_swap_max_width_range=(100, 120)
    # InkColorSwap.ink_swap_min_height_range is a pair of ints/floats determining the minimum height of the contour
    ink_swap_min_height_range=(2, 3)
    # InkColorSwap.ink_swap_max_height_range is a pair of ints/floats determining the maximum height of the contour
    ink_swap_max_height_range=(100, 120)
    # InkColorSwap.ink_swap_min_area_range is a pair of ints/floats determining the minimum area of the contour
    ink_swap_min_area_range=(10, 20)
    # InkColorSwap.ink_swap_max_area_range is a pair of ints/floats determining the maximum area of the contour
    ink_swap_max_area_range=(400, 500)

    # InkMottling.ink_mottling_alpha_range is a tuple of floats determining the alpha value of the mottling effect
    ink_mottling_alpha_range = (0.1, 0.2)
    # InkMottling.ink_mottling_noise_scale_range is a tuple of ints determining the size of Gaussian noise pattern
    ink_mottling_noise_scale_range = (1,2)
    # InkMottling.ink_mottling_gaussian_kernel_range is a tuple of ints determining the Gaussian kernel value
    ink_mottling_gaussian_kernel_range = (3,5)
    # InkMottling.p is the probability to run this augmentation.
    ink_mottling_p = 0.5

    # Jpeg.quality_range determines the range from which to sample compression level
    jpeg_quality_range = (25, 95)

    # Letterpress.n_samples is a tuple determining how many points to generate per cluster
    letterpress_n_samples = (100, 300)
    # Letterpress.n_clusters is a tuple determining how many clusters to generate
    letterpress_n_clusters = (300, 400)
    # Letterpress.std_range is a pair of ints determining the std deviation range in each blob
    letterpress_std_range = (500, 3000)
    # Letterpress.value_range determines values that points in the blob are sampled from
    letterpress_value_range = (150, 224)
    # Letterpress.value_threshold_range is the minimum pixel value to enable the effect (e.g. 128)
    letterpress_value_threshold_range = (96, 128)
    # Letterpress.blur enables blur in the noise mask
    letterpress_blur = 1
    # Letterpress.p is the probability to run this augmentation
    letterpress_p = (random.random() > 0.5) * 1

    # LightingGradient.mask_size determines how big the mask should be
    lightinggradient_light_position = None
    # LightingGradient.direction indicates the rotation degree of the light strip
    lightinggradient_direction = None
    # LightingGradient.max_brightness and LightingGradient.min_brightness set bounds for how much brightness change will happen
    lightinggradient_max_brightness = 196
    lightinggradient_min_brightness = 0
    # LightingGradient.mode is linear or gaussian depending on how light should decay
    lightinggradient_mode = random.choice(["linear_dynamic", "linear_static", "gaussian"])
    # LightingGradient.linear_decay_rate is only valid in linear static mode
    lightinggradient_linear_decay_rate = None
    # LightingGradient.transparency gives the transparency of the input image
    lightinggradient_transparency = None

    # LinesDegradation.line_roi is a tuple of 4 (x0, y0, xn, yn) to determine the region of interest of the augmentation effect
    lines_degradation_line_roi=(0.0, 0.0, 1.0, 1.0)
    # LinesDegradation.line_gradient_range is a pair of ints determining range of gradient values (low, high) in detecting the lines
    lines_degradation_line_gradient_range=(32, 255)
    # LinesDegradation.line_gradient_direction is a flag to set gradient gradient: 0 for horizontal gradients, 1 for vertical gradients and 2 for both
    lines_degradation_line_gradient_direction=(0, 2)
    # LinesDegradation.line_split_probability is a pair of floats determining the probability to split long line into shorter lines
    lines_degradation_line_split_probability=(0.2, 0.4)
    # LinesDegradation.line_replacement_value is a pair of ints determining the new value of the detected lines
    lines_degradation_line_replacement_value=random.choice([(5, 10),(250, 255)])
    # LinesDegradation.line_min_length is a pair of ints determining the minimum length of detected lines
    lines_degradation_line_min_length=(30, 40)
    # LinesDegradation.line_long_to_short_ratio is a pair of ints determining the threshold ratio of major axis to minor axis of the detected lines
    lines_degradation_line_long_to_short_ratio=(5, 7)
    # LinesDegradation.line_replacement_probability is a pair of floats determining the probability to replace the detected lines with new value
    lines_degradation_line_replacement_probability=(0.4, 0.5)
    # LinesDegradation.line_replacement_thickness is a pair of ints determining the thickness of replaced lines
    lines_degradation_line_replacement_thickness=(1, 3)

    # LowInkLines.count_range is a pair determining how many lines should be drawn
    lowinkrandomlines_count_range = (3, 12)
    lowinkperiodiclines_count_range = (1, 2)
    # LowInkLines.use_consistent_lines is false if we should vary the width and alpha of lines
    lowinkrandomlines_use_consistent_lines = random.choice([True, False])
    lowinkperiodiclines_use_consistent_lines = random.choice([True, False])
    # LowInkPeriodicLines.period_range is a pair determining how wide the gap between lines can be
    lowinkperiodiclines_period_range = (8, 32)
    # LowInkPeriodicLines.noise_probability is the probability to add noise into the generated lines
    lowinkperiodiclines_noise_probability = random.uniform(0.1, 0.2)
    # LowInkRandomLines.noise_probability is the probability to add noise into the generated lines
    lowinkrandomlines_noise_probability = random.uniform(0.1, 0.2)

    # Markup.num_lines_range determines how many lines get marked up
    markup_num_lines_range = (2, 7)
    # Markup.length_range determines the relative length of the drawn effect
    markup_length_range = (0.5, 1)
    # Markup.thickness_range determines the thickness of the drawn effect
    markup_thickness_range = (1, 1)
    # Markup.type determines the style of effect
    markup_type = random.choice(["strikethrough", "crossed", "highlight", "underline"])
    # Markup.ink determines the ink of markup effect
    markup_ink = random.choice(["pencil", "pen", "marker", "highlighter"])
    # Markup.color is the color of the ink used to markup
    markup_color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )
    # Markup.large_word_mode determines whether to draw markup on large words, else large word will be ignored.
    markup_large_word_mode = random.choice([True, False])
    # Markup.single_word_mode determines whether to draw across multiple words
    markup_single_word_mode = random.choice([True, False])
    # Markup.repetitions determines the number of times the effect is drawn
    markup_repetitions = random.randint(1, 2) if markup_type == "highlight" else 1
    # Markup.p is the probability to run this augmentation
    markup_p = (random.random() > 0.5) * 1

    # NoiseTexturize.sigma_range defines bounds of noise fluctuations
    noisetexturize_sigma_range = (3, 10)
    # NoiseTexturize.turbulence_range defines how quickly big patterns are replaced with small ones; lower means more iterations
    noisetexturize_turbulence_range = (2, 5)

    # PageBorder.page_border_width_height determines the width and height of page border effect
    page_border_width_height = "random"
    # PageBorder.page_border_color determines color of page border effect
    page_border_color = (0, 0, 0)
    # PageBorder.page_border_background_color determines color of page border background
    page_border_background_color = (0, 0, 0)
    # PageBorder.page_numbers determines  how many pages to render
    page_border_page_numbers = random.randint(4,12)
    # PageBorder.page_numbers determines  how many pages to render
    page_border_rotation_angle_range = (0,0)
    # PageBorder.curve_frequency determines frequency of curvy page shadow
    page_border_curve_frequency = (2, 8)
    # PageBorder.curve_height determines height of curvy page shadow
    page_border_curve_height = (2, 4)
    # PageBorder.curve_length_one_side determines Length for one side of generated curvy page shadow
    page_border_curve_length_one_side = (10, 50)
    # PageBorder.same_page_border determines whether the border will be in a same page
    page_border_same_page_border = 1

    # PatternGenerator.imgx is the width of the pattern image
    pattern_generator_imgx=random.randint(256,512) 
    # PatternGenerator.imgy is the height of the pattern image
    pattern_generator_imgy=random.randint(256,512)
    # PatternGenerator.n_rotation_range is a tuple determining the number of rotations applied to the pattern
    pattern_generator_n_rotation_range=(5, 15)

    # ReflectedLight.reflected_light_smoothness is a pair of floats determining the smoothness of ellipse
    reflected_light_smoothness=0.8
    # ReflectedLight.reflected_light_internal_radius_range is a pair of ints determining the major length of non fading area (centroid) of ellipse
    reflected_light_internal_radius_range=(0.0, 0.001)
    # ReflectedLight.reflected_light_external_radius_range is a pair of ints determining the major length of fading area of ellipse
    reflected_light_external_radius_range=(0.1, 0.8)
    # ReflectedLight.reflected_light_minor_major_ratio_range is a pair of floats determining the ratio of minor length to major length of the ellipse
    reflected_light_minor_major_ratio_range=(0.9, 1.0)
    # ReflectedLight.reflected_light_color is the color of the effect in BGR
    reflected_light_color=(180, 180, 180)
    # ReflectedLight.reflected_light_internal_max_brightness_range is a pair of floats determining the max brightness of the internal ellipse
    reflected_light_internal_max_brightness_range=(0.75, 0.75)
    # ReflectedLight.reflected_light_external_max_brightness_range is a pair of floats determining the max brightness of the external ellipse
    reflected_light_external_max_brightness_range=(0.5, 0.75)
    # ReflectedLight.reflected_light_location is the location of the effect
    reflected_light_location="random"
    # ReflectedLight.reflected_light_ellipse_angle_range is a pair of ints determining the angle of the ellipse
    reflected_light_ellipse_angle_range=(0, 360)
    # ReflectedLight.reflected_light_gaussian_kernel_size_range is a pair of ints determining the Gaussian kernel value
    reflected_light_gaussian_kernel_size_range=(5, 310)

    # Scribbles.scribbles_type determines the types of scribbles effect
    scribbles_scribbles_type = "lines"
    # Scribbles.scribbles_ink determines the types of scribbles ink
    scribbles_scribbles_ink = "random"
    # Scribbles.scribbles_location determines the location of scribbles effect
    scribbles_scribbles_location = "random"
    # Scribbles.scribbles_size_range determines the size of scribbles to draw
    scribbles_scribbles_size_range = (300, 700)
    # Scribbles.scribbles_count_range determines how many scribbles to draw
    scribbles_scribbles_count_range = (2, 3)
    # Scribbles.scribbles_thickness_range determines how thick scribbles are
    scribbles_scribbles_thickness_range = (2, 6)
    # Scribbles.scribbles_brightness_change is the brightness value of each stroke
    scribbles_scribbles_brightness_change = [0]
    # Scribbles.scribbles_pencil_skeletonize enable skeletonization effect in the scribbles
    scribbles_scribbles_skeletonize = 0
    # Scribbles.scribbles_skeletonize_iterations determine the number of skeletonizate iterations
    scribbles_scribbles_skeletonize_iterations = (1,1)
    # Scribbles.scribbles_color is the  color of scribbles
    scribbles_scribbles_color = (0, 0, 0)
    # Scribbles.scribbles_text is the text value for text based scribbles.
    scribbles_scribbles_text = "random"  
    # Scribbles.scribbles_text_font is the font types for text based scribbles.
    scribbles_scribbles_text_font = "random"
    # Scribbles.scribbles_text_rotate_range is the rotation angle of text based scribbles.
    scribbles_scribbles_text_rotate_range = (0,360)
    # Scribbles.scribbles_lines_stroke_count_range determines how many strokes per line scribble
    scribbles_scribbles_lines_stroke_count_range = (1, 2)
    # Scribbles.p is the probability to run this augmentation
    scribbles_p = (random.random() > 0.5) * 1

    # ShadowCast.shadow_side
    shadow_side="random"
    # ShadowCast.shadow_vertices_range
    shadow_vertices_range=(1, 20)
    # ShadowCast.shadow_width_range
    shadow_width_range=(0.3, 0.8)
    # ShadowCast.shadow_height_range
    shadow_height_range=(0.3, 0.8)
    # ShadowCast.shadow_color
    shadow_color=(64, 64, 64)
    # ShadowCast.shadow_opacity_range
    shadow_opacity_range=(0.2, 0.9)
    # ShadowCast.shadow_iterations_range
    shadow_iterations_range=(1, 2)
    # ShadowCast.shadow_blur_kernel_range
    shadow_blur_kernel_range=(101, 301)
    # ShadowCast.p is the probability to run this augmentation
    shadow_cast_p = (random.random() > 0.5) * 1
    
    # SubleNoise.range gives the variation range for sampling noise
    subtlenoise_range = 10

    # VoronoiTessellation.mult_range is the range of  amplification factor to generate Perlin noise
    voronoi_tessellation_mult_range=(50, 80)
    # VoronoiTessellation.seed is the seed value to generate Perlin Noise
    voronoi_tessellation_seed=random.randint(0,99999)
    # VoronoiTessellation.num_cells_range is the range for the number of cells used to generate the Voronoi Tessellation
    voronoi_tessellation_num_cells_range=(100, 1000)
    # VoronoiTessellation.noise_type is the noise type in the effect
    voronoi_tessellation_noise_type="random"
    # VoronoiTessellation.background_value is the range of background color assigned to each point
    voronoi_tessellation_background_value=(200, 255)

    # PaperFactory.texture_path is the directory to pull textures from
    paperfactory_texture_path = "./paper_textures"
    
    if badphotocopy_p > 0 or dirtyrollers_p > 0 or dirtydrum_p > 0 or markup_p > 0 or scribbles_p > 0 or shadow_cast_p > 0:
        faxify_monochrome_method = "grayscale"
        ink_mottling_p = 1
        
    if dithering_p or faxify_halftone:
        letterpress_p = 0
        if dithering_p:
            faxify_halftone = 0

    ################################################################################
    # PIPELINE
    #
    # The default Augraphy pipeline is defined in parametric form here.
    ################################################################################

    ink_phase = [
              
        InkColorSwap(
            ink_swap_color=ink_swap_color,
            ink_swap_sequence_number_range=ink_swap_sequence_number_range,
            ink_swap_min_width_range=ink_swap_min_width_range,
            ink_swap_max_width_range=ink_swap_max_width_range,
            ink_swap_min_height_range=ink_swap_min_height_range,
            ink_swap_max_height_range=ink_swap_max_height_range,
            ink_swap_min_area_range=ink_swap_min_area_range,
            ink_swap_max_area_range=ink_swap_max_area_range,
            p=0.5
        ),
                
        LinesDegradation(
            line_roi=lines_degradation_line_roi,
            line_gradient_range=lines_degradation_line_gradient_range,
            line_gradient_direction=lines_degradation_line_gradient_direction,
            line_split_probability=lines_degradation_line_split_probability,
            line_replacement_value=lines_degradation_line_replacement_value,
            line_min_length=lines_degradation_line_min_length,
            line_long_to_short_ratio=lines_degradation_line_long_to_short_ratio,
            line_replacement_probability=lines_degradation_line_replacement_probability,
            line_replacement_thickness=lines_degradation_line_replacement_thickness,
            p=0.5
        ),

        OneOf(
            [
                Dithering(
                    dither=dithering_dither_type,
                    order=dithering_order,
                    p=dithering_p,
                ),
                InkBleed(
                    intensity_range=inkbleed_intensity_range,
                    kernel_size=inkbleed_kernel_size,
                    severity=inkbleed_severity,
                    p=inkbleed_p,
                ),
            ],
            p=1,
        ),
        OneOf(
            [
                LowInkRandomLines(
                    count_range=lowinkrandomlines_count_range,
                    use_consistent_lines=lowinkrandomlines_use_consistent_lines,
                    noise_probability=lowinkrandomlines_noise_probability,
                    p=0.5,
                ),
                LowInkPeriodicLines(
                    count_range=lowinkperiodiclines_count_range,
                    period_range=lowinkperiodiclines_period_range,
                    use_consistent_lines=lowinkperiodiclines_use_consistent_lines,
                    noise_probability=lowinkperiodiclines_noise_probability,
                    p=0.5,
                ),
                Letterpress(
                    n_samples=letterpress_n_samples,
                    n_clusters=letterpress_n_clusters,
                    std_range=letterpress_std_range,
                    value_range=letterpress_value_range,
                    value_threshold_range=letterpress_value_threshold_range,
                    blur=letterpress_blur,
                    p=letterpress_p,
                ),
            ],
            p=1,
        ),
    ]

    paper_phase = [
        PaperFactory(
            texture_path=paperfactory_texture_path,
            p=1,
        ),
                
        OneOf(
            [
                DelaunayTessellation(
                    n_points_range=delaunay_tessellation_n_points_range,
                    n_horizontal_points_range=delaunay_tessellation_n_horizontal_points_range,
                    n_vertical_points_range=delaunay_tessellation_n_vertical_points_range,
                    noise_type=delaunay_tessellation_noise_type,
                    p=0.5,
                ),
                PatternGenerator(
                    imgx=pattern_generator_imgx,
                    imgy=pattern_generator_imgy,
                    n_rotation_range=pattern_generator_n_rotation_range,
                    p=0.5,
                ),
                VoronoiTessellation(
                    mult_range=voronoi_tessellation_mult_range,
                    seed=voronoi_tessellation_seed,
                    num_cells_range=voronoi_tessellation_num_cells_range,
                    noise_type=voronoi_tessellation_noise_type,
                    background_value=voronoi_tessellation_background_value,
                    p=0.5,
                ),          
            ],
            p=1,
        ),
        
                
        ColorPaper(
            hue_range=colorpaper_hue_range,
            saturation_range=colorpaper_saturation_range,
            p=0.5,
        ),
                         
            
        OneOf(
            [
                AugmentationSequence(
                    [
                        NoiseTexturize(
                            sigma_range=noisetexturize_sigma_range,
                            turbulence_range=noisetexturize_turbulence_range,
                            p=0.5,
                        ),
                        BrightnessTexturize(
                            texturize_range=brightnesstexturize_range,
                            deviation=brightnesstexturize_deviation,
                            p=0.5,
                        ),
                    ],
                ),
                AugmentationSequence(
                    [
                        BrightnessTexturize(
                            texturize_range=brightnesstexturize_range,
                            deviation=brightnesstexturize_deviation,
                            p=0.5,
                        ),
                        NoiseTexturize(
                            sigma_range=noisetexturize_sigma_range,
                            turbulence_range=noisetexturize_turbulence_range,
                            p=0.5,
                        ),
                    ],
                ),
            ],
            p=0.5,
        ),
    ]

    post_phase = [


        ColorShift(
            color_shift_offset_x_range=color_shift_offset_x_range,
            color_shift_offset_y_range=color_shift_offset_y_range,
            color_shift_iterations=color_shift_iterations,
            color_shift_brightness_range=color_shift_brightness_range,
            color_shift_gaussian_kernel_range=color_shift_gaussian_kernel_range,
            p=0.5,
        ), 
             
        BindingsAndFasteners(
            overlay_types=bindingsandfasteners_overlay_types,
            foreground=bindingsandfasteners_foreground,
            effect_type=bindingsandfasteners_effect_type,
            ntimes=bindingsandfasteners_ntimes,
            nscales=bindingsandfasteners_nscales,
            edge=bindingsandfasteners_edge,
            edge_offset=bindingsandfasteners_edge_offset,
            p=0.5,
        ),   
                
        Markup(
            num_lines_range=markup_num_lines_range,
            markup_length_range=markup_length_range,
            markup_thickness_range=markup_thickness_range,
            markup_type=markup_type,
            markup_ink=markup_ink,
            markup_color=markup_color,
            large_word_mode=markup_large_word_mode,
            single_word_mode=markup_single_word_mode,
            repetitions=markup_repetitions,
            p=0.5,
        ),
        OneOf(
            [     
                PageBorder( 
                    page_border_width_height =page_border_width_height,
                    page_border_color=page_border_color,
                    page_border_background_color=page_border_background_color,
                    page_numbers=page_border_page_numbers,
                    page_rotation_angle_range=page_border_rotation_angle_range,
                    curve_frequency=page_border_curve_frequency,
                    curve_height=page_border_curve_height,
                    curve_length_one_side=page_border_curve_length_one_side,
                    same_page_border=page_border_same_page_border,
                    p=1,
                ),
                DirtyRollers(
                    line_width_range=dirtyrollers_line_width_range,
                    scanline_type=dirtyrollers_scanline_type,
                    p=dirtyrollers_p,
                ),
            ],
            p=0.5,
        ),
        OneOf(
            [
                LightingGradient(
                    light_position=lightinggradient_light_position,
                    direction=lightinggradient_direction,
                    max_brightness=lightinggradient_max_brightness,
                    min_brightness=lightinggradient_min_brightness,
                    mode=lightinggradient_mode,
                    linear_decay_rate=lightinggradient_linear_decay_rate,
                    transparency=lightinggradient_transparency,
                    p=0.5,
                ),
                Brightness(
                    brightness_range=brightness_range,
                    min_brightness=brightness_min_brightness,
                    min_brightness_value=brightness_min_brightness_value,
                    p=0.5,
                ),
                Gamma(
                    gamma_range=gamma_range,
                    p=0.5,
                ),                 
            ],
            p=0.5,
        ),
        SubtleNoise(
            subtle_range=subtlenoise_range,
            p=0.5,
        ),
        Jpeg(
            quality_range=jpeg_quality_range,
            p=0.5,
        ),
        Scribbles(
            scribbles_type=scribbles_scribbles_type,
            scribbles_ink=scribbles_scribbles_ink,
            scribbles_location=scribbles_scribbles_location,
            scribbles_size_range=scribbles_scribbles_size_range,
            scribbles_count_range=scribbles_scribbles_count_range,
            scribbles_thickness_range=scribbles_scribbles_thickness_range,
            scribbles_brightness_change=scribbles_scribbles_brightness_change,
            scribbles_skeletonize=scribbles_scribbles_skeletonize,
            scribbles_skeletonize_iterations=scribbles_scribbles_skeletonize_iterations,
            scribbles_color=scribbles_scribbles_color,
            scribbles_text=scribbles_scribbles_text,
            scribbles_text_font=scribbles_scribbles_text_font,
            scribbles_text_rotate_range=scribbles_scribbles_text_rotate_range,
            scribbles_lines_stroke_count_range=scribbles_scribbles_lines_stroke_count_range,

            p=scribbles_p,  
        ),
        
          
        OneOf(
            [
                ShadowCast(
                    shadow_side=shadow_side,
                    shadow_vertices_range=shadow_vertices_range,
                    shadow_width_range=shadow_width_range,
                    shadow_height_range=shadow_height_range,
                    shadow_color=shadow_color,
                    shadow_opacity_range=shadow_opacity_range,
                    shadow_iterations_range=shadow_iterations_range,
                    shadow_blur_kernel_range=shadow_blur_kernel_range,
                    p=shadow_cast_p,
                ),
                        
                BadPhotoCopy(
                    noise_mask=badphotocopy_noise_mask,
                    noise_type=badphotocopy_noise_type,
                    noise_side=badphotocopy_noise_side,
                    noise_iteration=badphotocopy_noise_iteration,
                    noise_size=badphotocopy_noise_size,
                    noise_value=badphotocopy_noise_value,
                    noise_sparsity=badphotocopy_noise_sparsity,
                    noise_concentration=badphotocopy_noise_concentration,
                    blur_noise=badphotocopy_blur_noise,
                    blur_noise_kernel=badphotocopy_blur_noise_kernel,
                    wave_pattern=badphotocopy_wave_pattern,
                    edge_effect=badphotocopy_edge_effect,
                    p=badphotocopy_p,
                ),
            ],
            p=1,
        ),

        InkMottling(
            ink_mottling_alpha_range=ink_mottling_alpha_range,
            ink_mottling_noise_scale_range=ink_mottling_noise_scale_range,
            ink_mottling_gaussian_kernel_range=ink_mottling_gaussian_kernel_range,
            p=ink_mottling_p,
        ),
        Geometric(
            scale=geometric_scale,
            translation=geometric_translation,
            fliplr=geometric_fliplr,
            flipud=geometric_flipud,
            crop=geometric_crop,
            rotate_range=geometric_rotate_range,
            randomize = geometric_randomize,
            p=0.5,
        ),             
             
        OneOf(
            [
                Faxify(
                    scale_range=faxify_scale_range,
                    monochrome=faxify_monochrome,
                    monochrome_method=faxify_monochrome_method,
                    monochrome_arguments=faxify_monochrome_arguments,
                    halftone=faxify_halftone,
                    invert=faxify_invert,
                    half_kernel_size=faxify_half_kernel_size,
                    angle=faxify_angle,
                    sigma=faxify_sigma,
                    p=0.5,
                ),
                DirtyDrum(
                    line_width_range=dirtydrum_line_width_range,
                    line_concentration=dirtydrum_line_concentration,
                    direction=dirtydrum_direction,
                    noise_intensity=dirtydrum_noise_intensity,
                    noise_value=dirtydrum_noise_value,
                    ksize=dirtydrum_ksize,
                    sigmaX=dirtydrum_sigmaX,
                    p=dirtydrum_p,
                ),
            ],
            p=0.5,
        ),
                    
        ReflectedLight(
            reflected_light_smoothness=reflected_light_smoothness,
            reflected_light_internal_radius_range=reflected_light_internal_radius_range,
            reflected_light_external_radius_range=reflected_light_external_radius_range,
            reflected_light_minor_major_ratio_range=reflected_light_minor_major_ratio_range,
            reflected_light_color=reflected_light_color,
            reflected_light_internal_max_brightness_range=reflected_light_internal_max_brightness_range,
            reflected_light_external_max_brightness_range=reflected_light_external_max_brightness_range,
            reflected_light_location=reflected_light_location,
            reflected_light_ellipse_angle_range=reflected_light_ellipse_angle_range,
            reflected_light_gaussian_kernel_size_range=reflected_light_gaussian_kernel_size_range,
            p=0.5,
        ),
            
        BleedThrough(
            intensity_range=bleedthrough_intensity_range,
            color_range=bleedthrough_color_range,
            ksize=bleedthrough_ksize,
            sigmaX=bleedthrough_sigmaX,
            alpha=bleedthrough_alpha,
            offsets=bleedthrough_offsets,
            p=0.5,
        ),
    ]

    return AugraphyPipeline(ink_phase=ink_phase, paper_phase=paper_phase, post_phase=post_phase, save_outputs=True, log=True)
