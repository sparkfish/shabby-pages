from augraphy import *
import os
import random
import cv2


################################################################################
# CONTROLLING VARIATION
#
# We can control the outputs of the pipeline by setting values here.
################################################################################

# Dithering.dither_type can be 'ordered' for ordered dithering or another string for floyd-steinberg dithering
dithering_dither_type = random.choice(["ordered", "floyd-steinberg"])
# Dithering.order determines the dimensions of the threshold map
dithering_order = random.choice(range(1,10))

# InkBleed.intensity_range is a tuple with bounds for bleed intensity to be selected from
inkbleed_intensity_range = (0.1, 0.2)
# InkBleed.color_range is a tuple with bounds for color noise
inkbleed_color_range = (0, 224)
# InkBleed.kernel_size determines the radius of the bleed effect
inkbleed_kernel_size = (5, 5)
# InkBleed.severity determines significance of bleed effect
inkbleed_severity=(0.4, 0.6)

# BleedThrough.intensity_range is a tuple with bounds for bleed intensity to be selected from
bleedthrough_intensity_range=(0.1, 0.2)
# BleedThrough.color_range is a tuple with bounds for color noise
bleedthrough_color_range=(0, 224)
# BleedThrough.ksize is a tuple of height/width pairs for sampling kernel size
bleedthrough_ksize=(17, 17)
# BleedThrough.sigmaX is the standard deviation of the kernel along the x-axis
bleedthrough_sigmaX=0
# BleedThrough.alpha is the intensity of the bleeding effect, recommended 0.1-0.5
bleedthrough_alpha=0.3
# BleedThrough.offsets is a pair of x and y distances to shift the bleed with
bleedthrough_offsets=(10, 20)

# Letterpress.n_samples is a tuple determining how many points to generate per cluster
letterpress_n_samples=(100, 200)
# Letterpress.n_clusters is a tuple determining how many clusters to generate
letterpress_n_clusters=(500, 1000)
# Letterpress.std_range is a pair of ints determining the std deviation range in each blob
letterpress_std_range=(500, 500)
# Letterpress.value_range determines values that points in the blob are sampled from
letterpress_value_range=(200, 255)
# Letterpress.value_threshold_range is the minimum pixel value to enable the effect (e.g. 128)
letterpress_value_threshold_range=(128, 128)
# Letterpress.blur enables blur in the noise mask
letterpress_blur=1

# LowInkLines.count_range is a pair determining how many lines should be drawn
lowinkrandomlines_count_range = (5, 10)
lowinkperiodiclines_count_range = (2, 5)
# LowInkLines.use_consistent_lines is false if we should vary the width and alpha of lines
lowinkrandomlines_use_consistent_lines=random.choice([True, False])
lowinkperiodiclines_use_consistent_lines=random.choice([True, False])
# LowInkPeriodicLines.period_range is a pair determining how wide the gap between lines can be
lowinkperiodiclines_period_range=(10, 30)

# PaperFactory.tile_texture_shape determines the range from which to sample texture dimensions
paperfactory_tile_texture_shape = (250, 250)
# PaperFactory.texture_path is the directory to pull textures from
paperfactory_texture_path = "./paper_textures"

# NoiseTexturize.sigma_range defines bounds of noise fluctuations
noisetexturize_sigma_range = (3, 10)
# NoiseTexturize.turbulence_range defines how quickly big patterns are replaced with small ones; lower means more iterations
noisetexturize_turbulence_range = (2, 5)

# BrightnessTexturize.range determines the value range of samples for the brightness matrix
brightnesstexturize_range = (0.9, 0.99)
# BrightnessTexturize.deviation is additional variation for the uniform sample
brightnesstexturize_deviation = 0.03

# Brightness.range is a pair of floats determining the brightness delta
brightness_range = (0.8, 1.4)

# PageBorder.side determines the page edge of the effect
pageborder_side = random.choice(["left", "top", "bottom", "right"])
# PageBorder.width_range determines border thickness
pageborder_width_range = (5, 30)
# PageBorder.pages determines how many page shadows to render
pageborder_pages = None # internally this is random.randint(2, 7)

# DirtyRollers.line_width_range determines the width of roller lines
dirtyrollers_line_width_range = (8, 12)
# DirtyRollers.scanline_type changes the background of lines
dirtyrollers_scanline_type = 0

# LightingGradient.mask_size determines how big the mask should be
lightinggradient_light_position = None
# LightingGradient.direction indicates the rotation degree of the light strip
lightinggradient_direction = None
# LightingGradient.max_brightness and LightingGradient.min_brightness set bounds for how much brightness change will happen
lightinggradient_max_brightness = 255
lightinggradient_min_brightness = 0
# LightingGradient.mode is linear or gaussian depending on how light should decay
lightinggradient_mode = random.choice(["linear_dynamic", "linear_static", "gaussian"])
# LightingGradient.linear_decay_rate is only valid in linear static mode
lightinggradient_linear_decay_rate = None
# LightingGradient.transparency gives the transparency of the input image
lightinggradient_transparency = None

# DirtyDrum.line_width_range determines the range from which drum line widths are sampled
dirtydrum_line_width_range = (2, 8)
# DirtyDrum.direction is 0 for horizontal, 1 for vertical, 2 for both
dirtydrum_direction = random.randint(0,2)
# DirtyDrum.noise_intensity changes how significant the effect is, recommended 0.8-1.0
dirtydrum_noise_intensity = 0.95
# DirtyDrum.ksize is a tuple of height/width pairs from which to sample kernel size
dirtydrum_ksize = (3, 3)
# DirtyDrum.sigmaX is the stdev of the kernel in the x direction
dirtydrum_sigmaX = 0

# SubleNoise.range gives the variation range for sampling noise
subtlenoise_range = 10

# Jpeg.quality_range determines the range from which to sample compression level
jpeg_quality_range = (25, 95)

# BindingsAndFasteners.overlay_types can be min, max, or mix
bindingsandfasteners_overlay_types = random.choice([
    "min", "max", "mix", "normal",
    "lighten", "darken", "addition", "subtract",
    "difference", "screen", "dodge", "multiply",
    "divide", "hard_light", "grain_extract",
    "grain_merge", "overlay"
])
# BindingsAndFasteners.foreground is the path to fg image or the image itself
bindingsandfasteners_foreground = None
# BindingsAndFasteners.effect_type is "punch_holes", "binding_holes", or "clips"
bindingsandfasteners_effect_type = random.choice(["punch_holes", "binding_holes", "clips"])
# BindingsAndFasteners.ntimes gives how many fg images to draw
bindingsandfasteners_ntimes = 3
# BindingsAndFasteners.nscales is the scale of the fg image size
bindingsandfasteners_nscales = (1,1)
# BindingsAndFasteners.edge gives the edge to place the images on
bindingsandfasteners_edge = random.choice(["left", "top", "bottom", "right"])
# BindingsAndFasteners.edge_offset is how far from the page edge to draw
bindingsandfasteners_edge_offset = 50

# Gamma.range is an interval from which to sample a gamma shift
gamma_range = (0.5, 1.5)

# Geometric.scale is a pair determining how to scale the image
geometric_scale = (1, 1)
# Geometric.translation is a pair determining where to translate the image
geometric_translation = (0, 0)
# Geometric.fliplr flips the image left and right
geometric_fliplr = random.choice([0,1])
# Geometric.flipud flips the image up and down
geometric_flipud = random.choice([0,1])
# Geometric.crop four points giving the corners of a crop region
geometric_crop = ()
# Geometric.rotate_range a pair determining the rotation angle sample range
geometric_rotate_range = (0, 0)


################################################################################
# PIPELINE
#
# The default Augraphy pipeline is defined in parametric form here.
################################################################################

ink_phase = [
    Dithering(dithering_dither_type,
              dithering_order,
              p=0.2),

    InkBleed(inkbleed_intensity_range,
             inkbleed_color_range,
             inkbleed_kernel_size,
             inkbleed_severity,
             p=1),

    BleedThrough(bleedthrough_intensity_range,
                 bleedthrough_color_range,
                 bleedthrough_ksize,
                 bleedthrough_sigmaX,
                 bleedthrough_alpha,
                 bleedthrough_offsets,
                 p=0.5),

    Letterpress(letterpress_n_samples,
                letterpress_n_clusters,
                letterpress_std_range,
                letterpress_value_range,
                letterpress_value_threshold_range,
                letterpress_blur,
                p=0.5),

    OneOf(
        [
            LowInkRandomLines(lowinkrandomlines_count_range,
                              lowinkrandomlines_use_consistent_lines),

            LowInkPeriodicLines(lowinkperiodiclines_count_range,
                                lowinkperiodiclines_period_range,
                                lowinkperiodiclines_use_consistent_lines),
        ],
    ),
]

paper_phase = [
    PaperFactory(paperfactory_tile_texture_shape,
                 paperfactory_texture_path,
                 p=0.5),
    OneOf(
        [
            AugmentationSequence(
                [
                    NoiseTexturize(noisetexturize_sigma_range,
                                   noisetexturize_sigma_range),

                    BrightnessTexturize(brightnesstexturize_range,
                                        brightnesstexturize_deviation),
                ],
            ),
            AugmentationSequence(
                [
                    BrightnessTexturize(brightnesstexturize_range,
                                        brightnesstexturize_deviation),
                    NoiseTexturize(noisetexturize_sigma_range,
                                   noisetexturize_sigma_range),
                ],
            ),
        ],
        p=0.5,
    ),

    Brightness(brightness_range,
               p=0.5),
]

post_phase = [
    BrightnessTexturize(brightnesstexturize_range,
                        brightnesstexturize_deviation,
                        p=0.5),

    OneOf(
        [
            PageBorder(pageborder_side,
                       pageborder_width_range,
                       pageborder_pages),
            DirtyRollers(dirtyrollers_line_width_range,
                         dirtyrollers_scanline_type)
        ],
        p=0.5),

    OneOf(
        [
            LightingGradient(lightinggradient_light_position,
                             lightinggradient_max_brightness,
                             lightinggradient_min_brightness,
                             lightinggradient_mode,
                             lightinggradient_linear_decay_rate,
                             lightinggradient_transparency),
            Brightness(brightness_range)
        ],
        p=0.5),

    DirtyDrum(dirtydrum_line_width_range,
              dirtydrum_direction,
              dirtydrum_noise_intensity,
              dirtydrum_ksize,
              dirtydrum_sigmaX,
              p=0.5),

    SubtleNoise(subtlenoise_range,
                p=0.5),

    Jpeg(jpeg_quality_range,
         p=0.5),

    Markup(p=0.5),

    PencilScribbles(p=0.5),

    BindingsAndFasteners(bindingsandfasteners_overlay_types,
                         bindingsandfasteners_foreground,
                         bindingsandfasteners_effect_type,
                         bindingsandfasteners_ntimes,
                         bindingsandfasteners_nscales,
                         bindingsandfasteners_edge,
                         bindingsandfasteners_edge_offset,
                         p=0.5),

    BadPhotoCopy(p=0.5),

    Gamma(gamma_range,
          p=0.5),

    Geometric(geometric_scale,
              geometric_translation,
              geometric_fliplr,
              geometric_flipud,
              geometric_crop,
              geometric_rotate_range,
              p=0.5),

    Faxify(p=0.5),
]

def get_pipeline():
    """ This makes things easier."""
    return AugraphyPipeline(ink_phase,paper_phase,post_phase)
