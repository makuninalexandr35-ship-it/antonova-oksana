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


/**
 * Editable site content.
 * Keeps the design in code while allowing the owner to change key business data in wp-admin.
 */
function antonova_register_content_settings() {
    $fields = array(
        'antonova_city',
        'antonova_h1',
        'antonova_lead',
        'antonova_cake_price',
        'antonova_telegram_url',
        'antonova_whatsapp_url',
        'antonova_phone_display',
        'antonova_phone_tel',
    );

    foreach ($fields as $field) {
        register_setting(
            'antonova_content_group',
            $field,
            array(
                'type' => 'string',
                'sanitize_callback' => 'sanitize_text_field',
                'default' => '',
            )
        );
    }
}
add_action('admin_init', 'antonova_register_content_settings');

function antonova_add_content_page() {
    add_menu_page(
        'Antonova — контент сайта',
        'Antonova',
        'manage_options',
        'antonova-content',
        'antonova_render_content_page',
        'dashicons-edit-page',
        3
    );
}
add_action('admin_menu', 'antonova_add_content_page');

function antonova_render_content_page() {
    if (!current_user_can('manage_options')) {
        return;
    }

    $fields = array(
        'antonova_city' => array('Город / строка над заголовком', 'Домашняя кондитерская · Москва'),
        'antonova_h1' => array('Главный заголовок', 'Торты и авторские десерты на заказ в Москве'),
        'antonova_lead' => array('Подзаголовок', 'Индивидуальные вкусы, оформление и внимание к каждой детали. От идеи и референса — до десерта, который станет частью вашего праздника.'),
        'antonova_cake_price' => array('Цена торта', '3000 ₽/кг'),
        'antonova_telegram_url' => array('Ссылка Telegram', 'https://t.me/antonovaov'),
        'antonova_whatsapp_url' => array('Ссылка WhatsApp', 'https://wa.me/79647281844'),
        'antonova_phone_display' => array('Телефон — как показывать', '+7 964 728-18-44'),
        'antonova_phone_tel' => array('Телефон — для ссылки tel:', '+79647281844'),
    );
    ?>
    <div class="wrap">
        <h1>Antonova — контент сайта</h1>
        <p>Здесь можно менять основные данные без редактирования кода. Дизайн темы при этом не меняется.</p>
        <form method="post" action="options.php">
            <?php settings_fields('antonova_content_group'); ?>
            <table class="form-table" role="presentation">
                <?php foreach ($fields as $key => $meta) :
                    $value = get_option($key, '');
                    if ($value === '') {
                        $value = $meta[1];
                    }
                ?>
                    <tr>
                        <th scope="row"><label for="<?php echo esc_attr($key); ?>"><?php echo esc_html($meta[0]); ?></label></th>
                        <td>
                            <input class="regular-text" type="text" id="<?php echo esc_attr($key); ?>" name="<?php echo esc_attr($key); ?>" value="<?php echo esc_attr($value); ?>">
                        </td>
                    </tr>
                <?php endforeach; ?>
            </table>
            <?php submit_button('Сохранить изменения'); ?>
        </form>
    </div>
    <?php
}

function antonova_content($key, $default) {
    $value = get_option($key, '');
    return $value !== '' ? $value : $default;
}
