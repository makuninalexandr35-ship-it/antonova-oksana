<?php
if (!defined('ABSPATH')) {
    exit;
}

function antonova_theme_setup() {
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('html5', array('search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script'));
}
add_action('after_setup_theme', 'antonova_theme_setup');

function antonova_theme_assets() {
    wp_enqueue_style(
        'antonova-google-fonts',
        'https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600&family=Prata&display=swap',
        array(),
        null
    );

    wp_enqueue_style(
        'antonova-style',
        get_stylesheet_uri(),
        array('antonova-google-fonts'),
        wp_get_theme()->get('Version')
    );

    wp_enqueue_script(
        'antonova-script',
        get_template_directory_uri() . '/script.js',
        array(),
        wp_get_theme()->get('Version'),
        true
    );
}
add_action('wp_enqueue_scripts', 'antonova_theme_assets', 20);

// Keep the first migration visually as close as possible to the static site.
function antonova_remove_unused_core_styles() {
    wp_dequeue_style('wp-block-library');
    wp_dequeue_style('wp-block-library-theme');
    wp_dequeue_style('global-styles');
    wp_dequeue_style('classic-theme-styles');
}
add_action('wp_enqueue_scripts', 'antonova_remove_unused_core_styles', 100);
