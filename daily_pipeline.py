from augraphy import *
from PIL import Image
import os
import random
import cv2
from glob import glob
import numpy as np

def get_pipeline():

    ################################################################################
    # CONTROLLING VARIATION
    #
    # We can control the outputs of the pipeline by setting values here.
    ################################################################################

    # Dithering.dither_type can be 'ordered' for ordered dithering or another string for floyd-steinberg dithering
    dithering_dither_type = random.choice(["ordered", "floyd-steinberg"])
    # Dithering.order determines the dimensions of the threshold map
    dithering_order = random.choice(range(3,10))
    # dithering.p is the probability to run this augmentation
    dithering_p = (random.random()>0.7) * 1

    # InkBleed.intensity_range is a tuple with bounds for bleed intensity to be selected from
    inkbleed_intensity_range = (0.1, 0.4)
    # InkBleed.color_range is a tuple with bounds for color noise
    inkbleed_color_range = (0, 32)
    # InkBleed.kernel_size determines the radius of the bleed effect
    inkbleed_kernel_size = random.choice([(7,7), (5, 5), (3,3)])
    # InkBleed.severity determines significance of bleed effect
    inkbleed_severity=(0.4, 0.6)
    # inkbleed.p is the probability to run this augmentation
    inkbleed_p = 0.5

    # Letterpress.n_samples is a tuple determining how many points to generate per cluster
    letterpress_n_samples=(100, 300)
    # Letterpress.n_clusters is a tuple determining how many clusters to generate
    letterpress_n_clusters=(300, 400)
    # Letterpress.std_range is a pair of ints determining the std deviation range in each blob
    letterpress_std_range=(500, 3000)
    # Letterpress.value_range determines values that points in the blob are sampled from
    letterpress_value_range=(150, 224)
    # Letterpress.value_threshold_range is the minimum pixel value to enable the effect (e.g. 128)
    letterpress_value_threshold_range=(96, 128)
    # Letterpress.blur enables blur in the noise mask
    letterpress_blur=1
    # Letterpress.p is the probability to run this augmentation
    letterpress_p = (random.random()>0.5) * 1

    # LowInkLines.count_range is a pair determining how many lines should be drawn
    lowinkrandomlines_count_range = (3, 12)
    lowinkperiodiclines_count_range = (1, 2)
    # LowInkLines.use_consistent_lines is false if we should vary the width and alpha of lines
    lowinkrandomlines_use_consistent_lines=random.choice([True, False])
    lowinkperiodiclines_use_consistent_lines=random.choice([True, False])
    # LowInkPeriodicLines.period_range is a pair determining how wide the gap between lines can be
    lowinkperiodiclines_period_range=(8, 32)

    # PaperFactory.texture_path is the directory to pull textures from
    paperfactory_texture_path = "./paper_textures"

    # PaperColor.hue_range is range of randomized hue value
    hue_value1 = random.randint(0,245)
    hue_value2 = hue_value1+10
    papercolor_hue_range = (hue_value1,hue_value2)
    # PaperColor.saturation_range is range randomized of saturation value
    papercolor_saturation_range = (10,40)

    # NoiseTexturize.sigma_range defines bounds of noise fluctuations
    noisetexturize_sigma_range = (3, 10)
    # NoiseTexturize.turbulence_range defines how quickly big patterns are replaced with small ones; lower means more iterations
    noisetexturize_turbulence_range = (2, 5)

    # BrightnessTexturize.range determines the value range of samples for the brightness matrix
    brightnesstexturize_range = (0.9, 0.99)
    # BrightnessTexturize.deviation is additional variation for the uniform sample
    brightnesstexturize_deviation = 0.03

    # Brightness.range is a pair of floats determining the brightness delta
    brightness_range = (0.9, 1.1)

    # PageBorder.side determines the page edge of the effect
    pageborder_side = random.choice(["left", "top", "bottom", "right"])
    # PageBorder.border_background_value determines value of created border background.
    pageborder_border_background_value = (230, 255)
    # PageBorder.flip_border determines whether to flip the created border 
    pageborder_flip_border = random.choice([0,1])
    # PageBorder.width_range determines border thickness
    pageborder_width_range = (5, 30)
    # PageBorder.pages determines how many page shadows to render
    pageborder_pages = random.randint(6, 8)
    # PageBorder.intensity_range determines the noises of the page shadow
    pageborder_intensity_range = (0.1, 0.2)
    # PageBorder.curve_frequency determines frequency of curvy page shadow
    pageborder_curve_frequency = (2, 8)
    # PageBorder.curve_height determines height of curvy page shadow
    pageborder_curve_height = (2, 4)
    # PageBorder.curve_length_one_side determines Length for one side of generated curvy page shadow
    pageborder_curve_length_one_side = (50, 100)
    # PageBorder.value determines value of generated page shadow
    pageborder_value = (32, 150)
    # PageBorder.same_page_border determines whether the border will be in a same page 
    pageborder_same_page_border=1

    # DirtyRollers.line_width_range determines the width of roller lines
    dirtyrollers_line_width_range = (2, 32)
    # DirtyRollers.scanline_type changes the background of lines
    dirtyrollers_scanline_type = 0
    # DirtyRollers.p is the probability to run this augmentation
    dirtyrollers_p = (random.random()>0.5) * 1

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

    # DirtyDrum.line_width_range determines the range from which drum line widths are sampled
    dirtydrum_line_width_range = (1, 6)
    # concentration of dirty drum line
    dirtydrum_line_concentration = np.random.uniform(0.05, 0.15)
    # DirtyDrum.direction is 0 for horizontal, 1 for vertical, 2 for both
    dirtydrum_direction = random.randint(0,2)
    # DirtyDrum.noise_intensity changes how significant the effect is, recommended 0.8-1.0
    dirtydrum_noise_intensity = np.random.uniform(0.6, 0.95)
    # DirtyDrum.noise_value determine the intensity of dirty drum noise
    dirtydrum_noise_value = (128, 224)
    # DirtyDrum.ksize is a tuple of height/width pairs from which to sample kernel size
    dirtydrum_ksize = random.choice([(3, 3),(5,5),(7,7)])
    # DirtyDrum.sigmaX is the stdev of the kernel in the x direction
    dirtydrum_sigmaX = 0
    # DirtyDrum.p is the probability to run this augmentation
    dirtydrum_p = (random.random()>0.5) * 1

    # SubleNoise.range gives the variation range for sampling noise
    subtlenoise_range = 10

    # Jpeg.quality_range determines the range from which to sample compression level
    jpeg_quality_range = (25, 95)

    # Markup.num_lines_range determines how many lines get marked up
    markup_num_lines_range=(2, 7)
    # Markup.length_range determines the relative length of the drawn effect
    markup_length_range=(0.5, 1)
    # Markup.thickness_range determines the thickness of the drawn effect
    markup_thickness_range=(1, 1)
    # Markup.type determines the style of effect
    markup_type=random.choice(["strikethrough", "crossed", "highlight", "underline"])
    # Markup.color is the color of the ink used to markup
    markup_color=(random.randint(0,255),
                  random.randint(0,255),
                  random.randint(0,255))
    # Markup.single_word_mode determines whether to draw across multiple words
    markup_single_word_mode=random.choice([True, False])
    # Markup.repetitions determines the number of times the effect is drawn
    markup_repetitions= random.randint(1,2) if markup_type == "highlight" else 1
    # Markup.p is the probability to run this augmentation
    markup_p = (random.random()>0.5) * 1

    # PencilScribbles.size_range determines the size of scribbles to draw
    pencilscribbles_size_range=(100, 700)
    # PencilScribbles.count_range determines how many scribbles to draw
    pencilscribbles_count_range=(1, 4)
    # PencilScribbles.stroke_count_range determines how many strokes per scribble
    pencilscribbles_stroke_count_range=(1, 1)
    # PencilScribbles.thickness_range determines how thick strokes are
    pencilscribbles_thickness_range=(2, 6)
    # PencilScribbles.brightness_change is the brightness value of each stroke
    pencilscribbles_brightness_change=random.randint(64,224)
    # PencilScribbles.p is the probability to run this augmentation
    pencilscribbles_p = (random.random()>0.5) * 1

    # BindingsAndFasteners.overlay_types can be min, max, or mix
    bindingsandfasteners_overlay_types = "darken"
    # BindingsAndFasteners.foreground is the path to fg image or the image itself
    bindingsandfasteners_foreground = None
    # BindingsAndFasteners.effect_type is "punch_holes", "binding_holes", or "clips"
    bindingsandfasteners_effect_type = random.choice(["punch_holes", "binding_holes", "clips"])
    # BindingsAndFasteners.ntimes gives how many fg images to draw
    bindingsandfasteners_ntimes = (10,20) if bindingsandfasteners_effect_type == "binding_holes" else (2,3)
    # BindingsAndFasteners.nscales is the scale of the fg image size
    bindingsandfasteners_nscales = (0.9,1)
    # BindingsAndFasteners.edge gives the edge to place the images on
    bindingsandfasteners_edge = "random"
    # BindingsAndFasteners.edge_offset is how far from the page edge to draw
    bindingsandfasteners_edge_offset = (10,50)

    # BadPhotoCopy.mask is a mask of noise to generate the effect with
    badphotocopy_mask=None
    # BadPhotoCopy.noise_type determines which mask pattern to use
    badphotocopy_noise_type=-1
    # BadPhotoCopy.noise_side determines where to add noise
    badphotocopy_noise_side="random"
    # BadPhotoCopy.noise_iteration determines how many times to apply noise in the mask
    badphotocopy_noise_iteration=(1, 2)
    # BadPhotoCopy.noise_size determines the scale of noise in the mask
    badphotocopy_noise_size=(1, 2)
    # BadPhotoCopy.noise_value determines the intensity of the noise
    badphotocopy_noise_value=(128, 196)
    # BadPhotoCopy.noise_sparsity determines the sparseness of noise
    badphotocopy_noise_sparsity=(0.3, 0.6)
    # BadPhotoCopy.noise_concentration determines the concentration of noise
    badphotocopy_noise_concentration=(0.1, 0.5)
    # BadPhotoCopy.blur_noise determines whether or or not to add blur
    badphotocopy_blur_noise=random.choice([0,1])
    # BadPhotoCopy.blur_noise_kernel gives the dimensions for the noise kernel
    badphotocopy_blur_noise_kernel=random.choice([(3, 3), (5, 5)])
    # BadPhotoCopy.wave_pattern enables the wave pattern in the noise mask
    badphotocopy_wave_pattern=random.choice([0,1])
    # BadPhotoCopy.edge_effect adds the Sobel edge effect to the noise mask
    badphotocopy_edge_effect=random.choice([0,1])
    # BadPhotoCopy.p is the probability to run this augmentation
    badphotocopy_p = (random.random()>0.5) * 1

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
    geometric_rotate_range = (0,0)

    # Faxify.scale_range is a pair of ints determining the scaling magnitude
    faxify_scale_range=(0.3, 0.6)
    # Faxify.monochrome determines whether the image will get the halftone effect
    faxify_monochrome=random.choice([0, 1])
    # Faxify.monochrome_method is the binarization method for applying the effect
    faxify_monochrome_method="random"
    # Faxify.monochrome_argument is the input arguments to the monochrome method
    faxify_monochrome_arguments = {}
    # Faxify.monochrome_threshold is the simple binarization threshold value
    faxify_halftone = random.choice((0, 1))
    # Faxify.invert determines whether to invert the grayscale value in halftone
    faxify_invert=1
    # Faxify.half_kernel_size is half the Gaussian kernel size for halftone
    faxify_half_kernel_size=(1, 1)
    # Faxify.angle is the angle of the halftone effect
    faxify_angle=(0, 360)
    # Faxify.sigma is the sigma value of the Gaussian kernel in the halftone effect
    faxify_sigma=(1,3)



    # BleedThrough.intensity_range is a tuple with bounds for bleed intensity to be selected from
    bleedthrough_intensity_range=(0.1, 0.2)
    # BleedThrough.color_range is a tuple with bounds for color noise
    bleedthrough_color_range=(32, 224)
    # BleedThrough.ksize is a tuple of height/width pairs for sampling kernel size
    bleedthrough_ksize=(17, 17)
    # BleedThrough.sigmaX is the standard deviation of the kernel along the x-axis
    bleedthrough_sigmaX=0
    # BleedThrough.alpha is the intensity of the bleeding effect, recommended 0.1-0.5
    bleedthrough_alpha=random.uniform(0.05,0.1)
    # BleedThrough.offsets is a pair of x and y distances to shift the bleed with
    bleedthrough_offsets=(10, 20)


    if badphotocopy_p>0 or dirtyrollers_p>0 or dirtydrum_p>0 or markup_p>0 or pencilscribbles_p>0:
        faxify_monochrome_method = "grayscale"
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
        OneOf([
                Dithering(dithering_dither_type,
                  dithering_order,
                  p=dithering_p),

                InkBleed(inkbleed_intensity_range,
                         inkbleed_color_range,
                         inkbleed_kernel_size,
                         inkbleed_severity,
                         p=inkbleed_p)
               ],
                p=1),

        OneOf(
            [
                LowInkRandomLines(lowinkrandomlines_count_range,
                                  lowinkrandomlines_use_consistent_lines),

                LowInkPeriodicLines(lowinkperiodiclines_count_range,
                                    lowinkperiodiclines_period_range,
                                    lowinkperiodiclines_use_consistent_lines),

                Letterpress(letterpress_n_samples,
                    letterpress_n_clusters,
                    letterpress_std_range,
                    letterpress_value_range,
                    letterpress_value_threshold_range,
                    letterpress_blur,
                    p=letterpress_p),
            ],
            p=1
        )




    ]

    paper_phase = [
        PaperFactory(paperfactory_texture_path,
                     p=1),

        ColorPaper(papercolor_hue_range,
                   papercolor_saturation_range,
                   p=0.5
                   ),

        OneOf(
            [
                AugmentationSequence(
                    [
                        NoiseTexturize(noisetexturize_sigma_range,
                                       noisetexturize_turbulence_range),

                        BrightnessTexturize(brightnesstexturize_range,
                                            brightnesstexturize_deviation),
                    ],
                ),
                AugmentationSequence(
                    [
                        BrightnessTexturize(brightnesstexturize_range,
                                            brightnesstexturize_deviation),
                        NoiseTexturize(noisetexturize_sigma_range,
                                       noisetexturize_turbulence_range),
                    ],
                ),
            ],
            p=0.5,
        ),

#        Brightness(brightness_range,
#                   p=0.5),
    ]

    post_phase = [

        Markup(num_lines_range=markup_num_lines_range,
               markup_length_range=markup_length_range,
               markup_thickness_range=markup_thickness_range,
               markup_type=markup_type,
               markup_color=markup_color,
               single_word_mode=markup_single_word_mode,
               repetitions=markup_repetitions,
               p=0.5),

#        BrightnessTexturize(brightnesstexturize_range,
#                            brightnesstexturize_deviation,
#                            p=0.5),
        OneOf(
            [
                PageBorder(pageborder_side,
                           pageborder_border_background_value,
                           pageborder_flip_border,
                           pageborder_width_range,
                           pageborder_pages,
                           pageborder_intensity_range,
                           pageborder_curve_frequency,
                           pageborder_curve_height,
                           pageborder_curve_length_one_side,
                           pageborder_value,
                           pageborder_same_page_border),
                DirtyRollers(dirtyrollers_line_width_range,
                             dirtyrollers_scanline_type,
                             p=dirtyrollers_p)
            ],
            p=0.5),

        OneOf(
            [
                LightingGradient(lightinggradient_light_position,
                                 lightinggradient_direction,
                                 lightinggradient_max_brightness,
                                 lightinggradient_min_brightness,
                                 lightinggradient_mode,
                                 lightinggradient_linear_decay_rate,
                                 lightinggradient_transparency),
                Brightness(brightness_range),
                Gamma(gamma_range,
                      p=0.5)
            ],
            p=0.5),



        SubtleNoise(subtlenoise_range,
                    p=0.5),

        Jpeg(jpeg_quality_range,
             p=0.5),



        PencilScribbles(size_range=pencilscribbles_size_range,
                        count_range=pencilscribbles_count_range,
                        stroke_count_range=pencilscribbles_stroke_count_range,
                        thickness_range=pencilscribbles_thickness_range,
                        brightness_change=pencilscribbles_brightness_change,
                        p=pencilscribbles_p),

        BindingsAndFasteners(bindingsandfasteners_overlay_types,
                             bindingsandfasteners_foreground,
                             bindingsandfasteners_effect_type,
                             bindingsandfasteners_ntimes,
                             bindingsandfasteners_nscales,
                             bindingsandfasteners_edge,
                             bindingsandfasteners_edge_offset,
                             p=0.5),

        BadPhotoCopy(mask=badphotocopy_mask,
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
                     p=badphotocopy_p),



        Geometric(geometric_scale,
                  geometric_translation,
                  geometric_fliplr,
                  geometric_flipud,
                  geometric_crop,
                  geometric_rotate_range,
                  p=0.5),

        OneOf(
                [
                    Faxify(scale_range=faxify_scale_range,
                           monochrome=faxify_monochrome,
                           monochrome_method=faxify_monochrome_method,
                           monochrome_arguments = faxify_monochrome_arguments,
                           halftone = faxify_halftone,
                           invert=faxify_invert,
                           half_kernel_size=faxify_half_kernel_size,
                           angle=faxify_angle,
                           sigma=faxify_sigma,
                           p=0.5),

                    DirtyDrum(dirtydrum_line_width_range,
                          dirtydrum_line_concentration,
                          dirtydrum_direction,
                          dirtydrum_noise_intensity,
                          dirtydrum_noise_value,
                          dirtydrum_ksize,
                          dirtydrum_sigmaX,
                          p=dirtydrum_p)
                ],
                p=0.5),

        BleedThrough(bleedthrough_intensity_range,
                     bleedthrough_color_range,
                     bleedthrough_ksize,
                     bleedthrough_sigmaX,
                     bleedthrough_alpha,
                     bleedthrough_offsets,
                     p=0.5)

        ]



    return AugraphyPipeline(ink_phase,paper_phase,post_phase,log=True)
