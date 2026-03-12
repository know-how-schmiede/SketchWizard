import adsk.core
import adsk.fusion
import json
import locale
import os
import re
import sys
from ...lib import fusionAddInUtils as futil
from ... import config
from ...version import VERSION

app = adsk.core.Application.get()
ui = app.userInterface

TRANSLATIONS = {
    'de': {
        'cmd_description': 'Exportiert eine Skizze oder eine ausgewaehlte Flaeche als DXF, SVG oder PDF.',
        'no_sketches': 'Keine Skizzen im aktiven Design gefunden.',
        'error_no_exportable_geometry': 'Die Skizze enthaelt keine exportierbare Geometrie.',
        'error_invalid_extent': 'Die Skizze hat keine gueltige Ausdehnung fuer den Export.',
        'error_no_active_design': 'Kein aktives Design verfuegbar.',
        'error_dxf_export_failed': 'DXF-Export fehlgeschlagen.',
        'error_command_definition': 'Die Befehlsdefinition konnte nicht erstellt werden.',
        'error_workspace_missing': 'Workspace {workspace_id} wurde nicht gefunden.',
        'error_panel_missing': 'Ziel-Panel {panel_id} wurde nicht gefunden.',
        'error_no_valid_face': 'Es wurde keine gueltige planare Flaeche ausgewaehlt.',
        'error_select_sketch_or_face': 'Bitte eine Skizze oder eine Flaeche auswaehlen.',
        'error_face_sketch_create': 'Skizze auf der ausgewaehlten Flaeche konnte nicht erstellt werden.',
        'error_face_projection': 'Die Kontur der ausgewaehlten Flaeche konnte nicht in die Skizze projiziert werden.',
        'log_started': 'gestartet',
        'label_logo': 'Logo',
        'label_sketches': 'Skizzen',
        'label_faces': 'Flaechen',
        'label_projection_mode': 'Projektionsart',
        'projection_mode_specified_objects': 'Angegebene Objekte',
        'projection_mode_bodies': 'Koerper',
        'label_deactivate_sketch': 'Skizze deaktivieren',
        'label_no_sketch': '-- Keine --',
        'prompt_select_face': 'Planare Flaeche eines Koerpers auswaehlen',
        'label_export_format': 'Exportformat',
        'label_output_path': 'Ausgabepfad',
        'label_output_path_select': 'Ausgabepfad waehlen',
        'dialog_select_output_folder': 'Ausgabeordner waehlen',
        'error_no_valid_sketch': 'Es wurde keine gueltige Skizze ausgewaehlt.',
        'error_select_output_path': 'Bitte einen gueltigen Ausgabepfad auswaehlen.',
        'error_output_path_create': 'Ausgabepfad kann nicht erstellt werden:\n{path}',
        'msg_export_success': 'Export erfolgreich:\n{path}',
        'msg_export_failed': 'Export fehlgeschlagen ({export_format}):\n{error}'
    },
    'en': {
        'cmd_description': 'Exports a sketch or a selected face as DXF, SVG, or PDF.',
        'no_sketches': 'No sketches found in the active design.',
        'error_no_exportable_geometry': 'The sketch contains no exportable geometry.',
        'error_invalid_extent': 'The sketch has no valid extent for export.',
        'error_no_active_design': 'No active design is available.',
        'error_dxf_export_failed': 'DXF export failed.',
        'error_command_definition': 'Command definition could not be created.',
        'error_workspace_missing': 'Workspace {workspace_id} was not found.',
        'error_panel_missing': 'Target panel {panel_id} was not found.',
        'error_no_valid_face': 'No valid planar face was selected.',
        'error_select_sketch_or_face': 'Please select a sketch or a face.',
        'error_face_sketch_create': 'Could not create a sketch on the selected face.',
        'error_face_projection': 'Could not project the selected face contour into the sketch.',
        'log_started': 'started',
        'label_logo': 'Logo',
        'label_sketches': 'Sketches',
        'label_faces': 'Faces',
        'label_projection_mode': 'Projection Type',
        'projection_mode_specified_objects': 'Specified Objects',
        'projection_mode_bodies': 'Bodies',
        'label_deactivate_sketch': 'Deactivate Sketch',
        'label_no_sketch': '-- None --',
        'prompt_select_face': 'Select a planar body face',
        'label_export_format': 'Export Format',
        'label_output_path': 'Output Path',
        'label_output_path_select': 'Select Output Path',
        'dialog_select_output_folder': 'Select Output Folder',
        'error_no_valid_sketch': 'No valid sketch was selected.',
        'error_select_output_path': 'Please select a valid output path.',
        'error_output_path_create': 'Output path cannot be created:\n{path}',
        'msg_export_success': 'Export successful:\n{path}',
        'msg_export_failed': 'Export failed ({export_format}):\n{error}'
    },
    'es': {
        'cmd_description': 'Exporta un boceto o una cara seleccionada como DXF, SVG o PDF.',
        'no_sketches': 'No se encontraron bocetos en el diseno activo.',
        'error_no_exportable_geometry': 'El boceto no contiene geometria exportable.',
        'error_invalid_extent': 'El boceto no tiene una extension valida para exportar.',
        'error_no_active_design': 'No hay un diseno activo disponible.',
        'error_dxf_export_failed': 'La exportacion DXF ha fallado.',
        'error_command_definition': 'No se pudo crear la definicion del comando.',
        'error_workspace_missing': 'No se encontro el espacio de trabajo {workspace_id}.',
        'error_panel_missing': 'No se encontro el panel de destino {panel_id}.',
        'error_no_valid_face': 'No se selecciono una cara plana valida.',
        'error_select_sketch_or_face': 'Seleccione un boceto o una cara.',
        'error_face_sketch_create': 'No se pudo crear un boceto en la cara seleccionada.',
        'error_face_projection': 'No se pudo proyectar el contorno de la cara seleccionada en el boceto.',
        'log_started': 'iniciado',
        'label_logo': 'Logo',
        'label_sketches': 'Bocetos',
        'label_faces': 'Caras',
        'label_projection_mode': 'Tipo de proyeccion',
        'projection_mode_specified_objects': 'Objetos indicados',
        'projection_mode_bodies': 'Cuerpos',
        'label_deactivate_sketch': 'Desactivar boceto',
        'label_no_sketch': '-- Ninguno --',
        'prompt_select_face': 'Seleccione una cara plana del cuerpo',
        'label_export_format': 'Formato de exportacion',
        'label_output_path': 'Ruta de salida',
        'label_output_path_select': 'Seleccionar ruta de salida',
        'dialog_select_output_folder': 'Seleccionar carpeta de salida',
        'error_no_valid_sketch': 'No se selecciono un boceto valido.',
        'error_select_output_path': 'Seleccione una ruta de salida valida.',
        'error_output_path_create': 'No se puede crear la ruta de salida:\n{path}',
        'msg_export_success': 'Exportacion correcta:\n{path}',
        'msg_export_failed': 'La exportacion fallo ({export_format}):\n{error}'
    },
    'fr': {
        'cmd_description': 'Exporte une esquisse ou une face selectionnee en DXF, SVG ou PDF.',
        'no_sketches': 'Aucune esquisse trouvee dans la conception active.',
        'error_no_exportable_geometry': 'L esquisse ne contient aucune geometrie exportable.',
        'error_invalid_extent': 'L esquisse n a pas de dimensions valides pour l export.',
        'error_no_active_design': 'Aucune conception active disponible.',
        'error_dxf_export_failed': 'Echec de l export DXF.',
        'error_command_definition': 'Impossible de creer la definition de la commande.',
        'error_workspace_missing': 'Espace de travail {workspace_id} introuvable.',
        'error_panel_missing': 'Panneau cible {panel_id} introuvable.',
        'error_no_valid_face': 'Aucune face plane valide n a ete selectionnee.',
        'error_select_sketch_or_face': 'Veuillez selectionner une esquisse ou une face.',
        'error_face_sketch_create': 'Impossible de creer une esquisse sur la face selectionnee.',
        'error_face_projection': 'Impossible de projeter le contour de la face selectionnee dans l esquisse.',
        'log_started': 'demarre',
        'label_logo': 'Logo',
        'label_sketches': 'Esquisses',
        'label_faces': 'Faces',
        'label_projection_mode': 'Type de projection',
        'projection_mode_specified_objects': 'Objets indiques',
        'projection_mode_bodies': 'Corps',
        'label_deactivate_sketch': 'Desactiver l esquisse',
        'label_no_sketch': '-- Aucune --',
        'prompt_select_face': 'Selectionner une face plane d un corps',
        'label_export_format': 'Format d export',
        'label_output_path': 'Chemin de sortie',
        'label_output_path_select': 'Choisir le chemin de sortie',
        'dialog_select_output_folder': 'Choisir le dossier de sortie',
        'error_no_valid_sketch': 'Aucune esquisse valide n a ete selectionnee.',
        'error_select_output_path': 'Veuillez selectionner un chemin de sortie valide.',
        'error_output_path_create': 'Impossible de creer le chemin de sortie:\n{path}',
        'msg_export_success': 'Export reussi:\n{path}',
        'msg_export_failed': 'Echec de l export ({export_format}):\n{error}'
    },
    'it': {
        'cmd_description': 'Esporta uno schizzo o una faccia selezionata come DXF, SVG o PDF.',
        'no_sketches': 'Nessuno schizzo trovato nel progetto attivo.',
        'error_no_exportable_geometry': 'Lo schizzo non contiene geometria esportabile.',
        'error_invalid_extent': 'Lo schizzo non ha dimensioni valide per l esportazione.',
        'error_no_active_design': 'Nessun progetto attivo disponibile.',
        'error_dxf_export_failed': 'Esportazione DXF non riuscita.',
        'error_command_definition': 'Impossibile creare la definizione del comando.',
        'error_workspace_missing': 'Workspace {workspace_id} non trovato.',
        'error_panel_missing': 'Pannello di destinazione {panel_id} non trovato.',
        'error_no_valid_face': 'Non e stata selezionata una faccia planare valida.',
        'error_select_sketch_or_face': 'Selezionare uno schizzo o una faccia.',
        'error_face_sketch_create': 'Impossibile creare uno schizzo sulla faccia selezionata.',
        'error_face_projection': 'Impossibile proiettare il contorno della faccia selezionata nello schizzo.',
        'log_started': 'avviato',
        'label_logo': 'Logo',
        'label_sketches': 'Schizzi',
        'label_faces': 'Facce',
        'label_projection_mode': 'Tipo di proiezione',
        'projection_mode_specified_objects': 'Oggetti indicati',
        'projection_mode_bodies': 'Corpi',
        'label_deactivate_sketch': 'Disattiva schizzo',
        'label_no_sketch': '-- Nessuno --',
        'prompt_select_face': 'Seleziona una faccia planare di un corpo',
        'label_export_format': 'Formato di esportazione',
        'label_output_path': 'Percorso di output',
        'label_output_path_select': 'Seleziona percorso di output',
        'dialog_select_output_folder': 'Seleziona cartella di output',
        'error_no_valid_sketch': 'Non e stato selezionato uno schizzo valido.',
        'error_select_output_path': 'Selezionare un percorso di output valido.',
        'error_output_path_create': 'Impossibile creare il percorso di output:\n{path}',
        'msg_export_success': 'Esportazione completata:\n{path}',
        'msg_export_failed': 'Esportazione non riuscita ({export_format}):\n{error}'
    },
    'pl': {
        'cmd_description': 'Eksportuje szkic lub wybrana powierzchnie jako DXF, SVG lub PDF.',
        'no_sketches': 'Nie znaleziono szkicow w aktywnym projekcie.',
        'error_no_exportable_geometry': 'Szkic nie zawiera geometrii do eksportu.',
        'error_invalid_extent': 'Szkic nie ma prawidlowego zakresu do eksportu.',
        'error_no_active_design': 'Brak aktywnego projektu.',
        'error_dxf_export_failed': 'Eksport DXF nie powiodl sie.',
        'error_command_definition': 'Nie mozna utworzyc definicji polecenia.',
        'error_workspace_missing': 'Nie znaleziono obszaru roboczego {workspace_id}.',
        'error_panel_missing': 'Nie znaleziono panelu docelowego {panel_id}.',
        'error_no_valid_face': 'Nie wybrano prawidlowej plaskiej powierzchni.',
        'error_select_sketch_or_face': 'Wybierz szkic lub powierzchnie.',
        'error_face_sketch_create': 'Nie mozna utworzyc szkicu na wybranej powierzchni.',
        'error_face_projection': 'Nie mozna rzutowac konturu wybranej powierzchni do szkicu.',
        'log_started': 'uruchomiono',
        'label_logo': 'Logo',
        'label_sketches': 'Szkice',
        'label_faces': 'Powierzchnie',
        'label_projection_mode': 'Typ rzutowania',
        'projection_mode_specified_objects': 'Wskazane obiekty',
        'projection_mode_bodies': 'Bryly',
        'label_deactivate_sketch': 'Wylacz szkic',
        'label_no_sketch': '-- Brak --',
        'prompt_select_face': 'Wybierz plaska powierzchnie bryly',
        'label_export_format': 'Format eksportu',
        'label_output_path': 'Sciezka wyjsciowa',
        'label_output_path_select': 'Wybierz sciezke wyjsciowa',
        'dialog_select_output_folder': 'Wybierz folder wyjsciowy',
        'error_no_valid_sketch': 'Nie wybrano prawidlowego szkicu.',
        'error_select_output_path': 'Wybierz prawidlowa sciezke wyjsciowa.',
        'error_output_path_create': 'Nie mozna utworzyc sciezki wyjsciowej:\n{path}',
        'msg_export_success': 'Eksport zakonczony:\n{path}',
        'msg_export_failed': 'Eksport nie powiodl sie ({export_format}):\n{error}'
    }
}

SUPPORTED_LANGUAGES = ('de', 'en', 'es', 'fr', 'it', 'pl')
DEFAULT_LANGUAGE = 'en'
FUSION_LANGUAGE_ENUM_NAMES = {
    'de': ('GermanLanguage', 'GermanUserLanguage'),
    'en': ('EnglishLanguage', 'EnglishUserLanguage'),
    'es': ('SpanishLanguage', 'SpanishUserLanguage'),
    'fr': ('FrenchLanguage', 'FrenchUserLanguage'),
    'it': ('ItalianLanguage', 'ItalianUserLanguage'),
    'pl': ('PolishLanguage', 'PolishUserLanguage')
}
LANGUAGE_KEYWORDS = (
    ('german', 'de'),
    ('deutsch', 'de'),
    ('english', 'en'),
    ('spanish', 'es'),
    ('espanol', 'es'),
    ('french', 'fr'),
    ('francais', 'fr'),
    ('italian', 'it'),
    ('italiano', 'it'),
    ('polish', 'pl'),
    ('polski', 'pl')
)


def _normalize_language_hint(language_hint):
    if not language_hint:
        return ''
    return str(language_hint).strip().lower().replace('-', '_')


def _map_language_hint(language_hint):
    normalized = _normalize_language_hint(language_hint)
    if not normalized:
        return ''

    normalized_parts = normalized.split('_')
    if normalized_parts and normalized_parts[0] in SUPPORTED_LANGUAGES:
        return normalized_parts[0]

    for keyword, language_code in LANGUAGE_KEYWORDS:
        if keyword in normalized:
            return language_code

    return ''


def _detect_language_from_fusion_preferences():
    try:
        preferences = getattr(app, 'preferences', None)
        general_preferences = getattr(preferences, 'generalPreferences', None)
        user_language = getattr(general_preferences, 'userLanguage', None)
        if user_language is None:
            return ''

        user_languages_enum = getattr(adsk.core, 'UserLanguages', None)
        if user_languages_enum is not None:
            for language_code, enum_names in FUSION_LANGUAGE_ENUM_NAMES.items():
                for enum_name in enum_names:
                    enum_value = getattr(user_languages_enum, enum_name, None)
                    if enum_value is not None and user_language == enum_value:
                        return language_code

        return _map_language_hint(user_language)
    except:
        return ''


def _detect_language_from_system():
    try:
        env_locale = os.environ.get('LC_ALL') or os.environ.get('LANG') or os.environ.get('LANGUAGE')
        detected_language = _map_language_hint(env_locale)
        if detected_language:
            return detected_language
    except:
        pass

    try:
        current_locale = locale.getlocale()[0]
        return _map_language_hint(current_locale)
    except:
        return ''


def _detect_language():
    fusion_language = _detect_language_from_fusion_preferences()
    if fusion_language:
        return fusion_language

    system_language = _detect_language_from_system()
    if system_language:
        return system_language

    return DEFAULT_LANGUAGE


LANGUAGE = _detect_language()


def tr(key: str, **kwargs):
    language_values = TRANSLATIONS.get(LANGUAGE, {})
    fallback_values = TRANSLATIONS.get('en', {})
    template = language_values.get(key, fallback_values.get(key, key))
    return template.format(**kwargs)


CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_cmdDialog'
CMD_NAME = f'SketchWizard {VERSION}'
CMD_Description = tr('cmd_description')

# Specify that the command will be promoted to the panel.
IS_PROMOTED = False

# Design > Solid > Create
WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_ID = 'SolidCreatePanel'
LEGACY_PANEL_IDS = [
    'SolidScriptsAddinsPanel',
    f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_DienstprogrammPanel'
]

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

LOGO_IMAGE_INPUT_ID = 'logo_image'
SKETCH_DROPDOWN_INPUT_ID = 'sketch_dropdown'
FACE_SELECTION_INPUT_ID = 'face_selection'
PROJECTION_MODE_DROPDOWN_INPUT_ID = 'projection_mode_dropdown'
FORMAT_DROPDOWN_INPUT_ID = 'export_format_dropdown'
OUTPUT_PATH_INPUT_ID = 'output_path'
OUTPUT_PATH_BUTTON_INPUT_ID = 'output_path_button'
DEACTIVATE_SKETCH_INPUT_ID = 'deactivate_sketch'

NO_SKETCHES_TEXT = tr('no_sketches')
NO_SKETCH_SELECTED_TEXT = tr('label_no_sketch')
PROJECTION_MODE_SPECIFIED_OBJECTS = 'specified_objects'
PROJECTION_MODE_BODIES = 'bodies'
SETTINGS_OUTPUT_PATH_KEY = 'output_path'
SETTINGS_FILENAME = 'settings.json'
SVG_STROKE_TOLERANCE_CM = 0.01  # 0.1 mm
PDF_PT_PER_MM = 72.0 / 25.4
EXPORT_SKETCH_NAME_PREFIX = 'Export'

# Local list of event handlers used to maintain a reference so
# they are not released and garbage collected.
local_handlers = []
sketch_objects_by_label = {}


def _settings_file_path():
    if os.name == 'nt':
        base_dir = os.environ.get('APPDATA', os.path.expanduser('~'))
        settings_dir = os.path.join(base_dir, 'SketchWizzard')
    elif sys.platform == 'darwin':
        settings_dir = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'SketchWizzard')
    else:
        settings_dir = os.path.join(os.path.expanduser('~'), '.config', 'SketchWizzard')
    return os.path.join(settings_dir, SETTINGS_FILENAME)


def _load_settings():
    settings_path = _settings_file_path()
    if not os.path.exists(settings_path):
        return {}

    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
    except:
        pass
    return {}


def _save_settings(settings: dict):
    settings_path = _settings_file_path()
    os.makedirs(os.path.dirname(settings_path), exist_ok=True)
    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=True, indent=2)


def _load_output_path():
    settings = _load_settings()
    output_path = settings.get(SETTINGS_OUTPUT_PATH_KEY, '')
    if output_path:
        return output_path
    return os.path.expanduser('~')


def _persist_output_path(output_path: str):
    settings = _load_settings()
    settings[SETTINGS_OUTPUT_PATH_KEY] = output_path
    _save_settings(settings)


def _get_logo_candidate_paths():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    appdata_dir = os.environ.get('APPDATA', '')
    appdata_addin_root = os.path.join(
        appdata_dir,
        'Autodesk',
        'Autodesk Fusion 360',
        'API',
        'AddIns',
        'SketchWizard'
    )
    addin_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..', '..'))
    module_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
    return [
        os.path.join(appdata_addin_root, 'images', 'Logo_SketchWizard_200.png'),
        os.path.join(addin_root, 'images', 'Logo_SketchWizard_200.png'),
        os.path.join(module_root, 'images', 'Logo_SketchWizard_200.png'),
        os.path.join(current_dir, 'resources', '64x64.png')
    ]


def _add_logo_input(inputs: adsk.core.CommandInputs):
    for candidate_path in _get_logo_candidate_paths():
        if not os.path.exists(candidate_path):
            continue

        try:
            logo_input = inputs.addImageCommandInput(LOGO_IMAGE_INPUT_ID, tr('label_logo'), candidate_path)
            return logo_input
        except:
            pass

    return None


def _remove_control_from_panel(panel: adsk.core.ToolbarPanel):
    if not panel:
        return
    control = panel.controls.itemById(CMD_ID)
    if control:
        control.deleteMe()


def _cleanup_legacy_controls(workspace: adsk.core.Workspace):
    if workspace is None:
        return

    for panel_id in LEGACY_PANEL_IDS:
        panel = workspace.toolbarPanels.itemById(panel_id)
        _remove_control_from_panel(panel)


def _get_active_design():
    return adsk.fusion.Design.cast(app.activeProduct)


def _collect_sketch_entries():
    design = _get_active_design()
    if design is None:
        return []

    raw_entries = []
    components = design.allComponents
    for i in range(components.count):
        component = components.item(i)
        if component is None:
            continue

        for j in range(component.sketches.count):
            sketch = component.sketches.item(j)
            if sketch is None:
                continue

            if component == design.rootComponent:
                label = sketch.name
            else:
                label = f'{component.name} / {sketch.name}'
            raw_entries.append((label, sketch))

    raw_entries.sort(key=lambda entry: entry[0].lower())

    unique_entries = []
    name_count = {}
    for base_label, sketch in raw_entries:
        count = name_count.get(base_label, 0) + 1
        name_count[base_label] = count
        label = base_label if count == 1 else f'{base_label} ({count})'
        unique_entries.append((label, sketch))

    return unique_entries


def _get_selected_sketch_label(inputs: adsk.core.CommandInputs):
    sketch_dropdown = adsk.core.DropDownCommandInput.cast(inputs.itemById(SKETCH_DROPDOWN_INPUT_ID))
    if sketch_dropdown is None or sketch_dropdown.selectedItem is None:
        return ''
    return sketch_dropdown.selectedItem.name


def _is_real_sketch_label(label: str):
    return bool(label) and label not in (NO_SKETCHES_TEXT, NO_SKETCH_SELECTED_TEXT)


def _select_dropdown_item(dropdown: adsk.core.DropDownCommandInput, target_name: str):
    if dropdown is None or not target_name:
        return False

    for index in range(dropdown.listItems.count):
        item = dropdown.listItems.item(index)
        if item and item.name == target_name:
            item.isSelected = True
            return True
    return False


def _set_sketch_dropdown_to_none(inputs: adsk.core.CommandInputs):
    sketch_dropdown = adsk.core.DropDownCommandInput.cast(inputs.itemById(SKETCH_DROPDOWN_INPUT_ID))
    if sketch_dropdown is None or not sketch_dropdown.isEnabled:
        return
    _select_dropdown_item(sketch_dropdown, NO_SKETCH_SELECTED_TEXT)


def _clear_face_selection(inputs: adsk.core.CommandInputs):
    face_input = adsk.core.SelectionCommandInput.cast(inputs.itemById(FACE_SELECTION_INPUT_ID))
    if face_input is None:
        return

    try:
        face_input.clearSelection()
    except:
        pass


def _get_selected_face(inputs: adsk.core.CommandInputs):
    face_input = adsk.core.SelectionCommandInput.cast(inputs.itemById(FACE_SELECTION_INPUT_ID))
    if face_input is None or face_input.selectionCount < 1:
        return None

    try:
        selection = face_input.selection(0)
        entity = selection.entity if selection else None
        face = adsk.fusion.BRepFace.cast(entity)
        if face and face.isValid:
            return face
    except:
        pass
    return None


def _has_valid_sketch_selection(inputs: adsk.core.CommandInputs):
    sketch_dropdown = adsk.core.DropDownCommandInput.cast(inputs.itemById(SKETCH_DROPDOWN_INPUT_ID))
    if sketch_dropdown is None or not sketch_dropdown.isEnabled:
        return False
    if sketch_dropdown.selectedItem is None:
        return False
    return _is_real_sketch_label(sketch_dropdown.selectedItem.name)


def _has_valid_face_selection(inputs: adsk.core.CommandInputs):
    return _get_selected_face(inputs) is not None


def _find_sketch_by_label(selected_label: str):
    if not _is_real_sketch_label(selected_label):
        return None

    sketch = sketch_objects_by_label.get(selected_label)
    if sketch and sketch.isValid:
        return sketch

    for entry_label, entry_sketch in _collect_sketch_entries():
        if entry_label == selected_label:
            return entry_sketch
    return None


def _get_selected_projection_mode(inputs: adsk.core.CommandInputs):
    projection_dropdown = adsk.core.DropDownCommandInput.cast(inputs.itemById(PROJECTION_MODE_DROPDOWN_INPUT_ID))
    if projection_dropdown is None or projection_dropdown.selectedItem is None:
        return PROJECTION_MODE_SPECIFIED_OBJECTS
    if projection_dropdown.selectedItem.name == tr('projection_mode_bodies'):
        return PROJECTION_MODE_BODIES
    return PROJECTION_MODE_SPECIFIED_OBJECTS


def _get_selected_format(inputs: adsk.core.CommandInputs):
    format_dropdown = adsk.core.DropDownCommandInput.cast(inputs.itemById(FORMAT_DROPDOWN_INPUT_ID))
    if format_dropdown and format_dropdown.selectedItem:
        return format_dropdown.selectedItem.name.upper()
    return 'DXF'


def _get_output_path(inputs: adsk.core.CommandInputs):
    output_path_input = adsk.core.StringValueCommandInput.cast(inputs.itemById(OUTPUT_PATH_INPUT_ID))
    if output_path_input:
        return output_path_input.value.strip()
    return ''


def _get_deactivate_sketch_option(inputs: adsk.core.CommandInputs):
    deactivate_input = adsk.core.BoolValueCommandInput.cast(inputs.itemById(DEACTIVATE_SKETCH_INPUT_ID))
    if deactivate_input is None:
        return False
    return bool(deactivate_input.value)


def _deactivate_sketch_in_browser(sketch: adsk.fusion.Sketch):
    if sketch is None or not sketch.isValid:
        return

    try:
        sketch.isLightBulbOn = False
        return
    except:
        pass

    try:
        sketch.isVisible = False
    except:
        pass


def _sanitize_filename(filename: str, fallback: str = 'sketch_export'):
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', filename or '')
    cleaned = cleaned.strip().strip('.')
    return cleaned or fallback


def _get_active_construction_name():
    document_name = ''
    try:
        active_document = getattr(app, 'activeDocument', None)
        document_name = getattr(active_document, 'name', '') if active_document else ''
    except:
        document_name = ''

    if document_name:
        return _sanitize_filename(os.path.splitext(document_name)[0], fallback='construction')

    try:
        design = _get_active_design()
        root_component = design.rootComponent if design else None
        if root_component and root_component.name:
            return _sanitize_filename(root_component.name, fallback='construction')
    except:
        pass

    return 'construction'


def _to_mm(value_in_cm: float):
    return value_in_cm * 10.0


def _format_float(value: float):
    text = f'{value:.6f}'.rstrip('0').rstrip('.')
    return text if text else '0'


def _points_close(point_a, point_b, tolerance=1e-5):
    return abs(point_a[0] - point_b[0]) <= tolerance and abs(point_a[1] - point_b[1]) <= tolerance


def _remove_duplicate_points(points):
    if not points:
        return []

    result = [points[0]]
    for point in points[1:]:
        if not _points_close(point, result[-1]):
            result.append(point)
    return result


def _sample_sketch_curve_points(sketch: adsk.fusion.Sketch, sketch_curve):
    try:
        if hasattr(sketch_curve, 'isConstruction') and sketch_curve.isConstruction:
            return []
        if hasattr(sketch_curve, 'isVisible') and not sketch_curve.isVisible:
            return []

        world_geometry = sketch_curve.worldGeometry
        if world_geometry is None:
            return []

        evaluator = world_geometry.evaluator
        if evaluator is None:
            return []

        success, start_param, end_param = evaluator.getParameterExtents()
        if not success:
            return []

        success, points_3d = evaluator.getStrokes(start_param, end_param, SVG_STROKE_TOLERANCE_CM)
        if not success or not points_3d:
            return []

        points_2d = []
        for point_3d in points_3d:
            sketch_point = sketch.modelToSketchSpace(point_3d)
            if sketch_point is None:
                continue
            points_2d.append((_to_mm(sketch_point.x), _to_mm(sketch_point.y)))

        return _remove_duplicate_points(points_2d)
    except:
        return []


def _collect_export_strokes(sketch: adsk.fusion.Sketch):
    strokes = []
    sketch_curves = sketch.sketchCurves
    for i in range(sketch_curves.count):
        sketch_curve = sketch_curves.item(i)
        if sketch_curve is None:
            continue
        stroke = _sample_sketch_curve_points(sketch, sketch_curve)
        if len(stroke) >= 2:
            strokes.append(stroke)

    if not strokes:
        return None, tr('error_no_exportable_geometry')

    all_x = [point[0] for stroke in strokes for point in stroke]
    all_y = [point[1] for stroke in strokes for point in stroke]

    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)

    if _points_close((min_x, min_y), (max_x, max_y)):
        return None, tr('error_invalid_extent')

    return {
        'strokes': strokes,
        'min_x': min_x,
        'max_x': max_x,
        'min_y': min_y,
        'max_y': max_y
    }, ''


def _export_sketch_as_svg(sketch: adsk.fusion.Sketch, output_file: str):
    export_data, error_message = _collect_export_strokes(sketch)
    if export_data is None:
        return False, error_message

    strokes = export_data['strokes']
    min_x = export_data['min_x']
    max_x = export_data['max_x']
    min_y = export_data['min_y']
    max_y = export_data['max_y']

    margin_mm = 1.0
    width_mm = (max_x - min_x) + (2.0 * margin_mm)
    height_mm = (max_y - min_y) + (2.0 * margin_mm)

    def map_x(x_value):
        return (x_value - min_x) + margin_mm

    def map_y(y_value):
        return (max_y - y_value) + margin_mm

    path_lines = []
    for stroke in strokes:
        transformed = [(map_x(x), map_y(y)) for x, y in stroke]
        if len(transformed) < 2:
            continue

        is_closed = _points_close(transformed[0], transformed[-1])
        if is_closed:
            transformed = transformed[:-1]
        if len(transformed) < 2:
            continue

        commands = [f'M {_format_float(transformed[0][0])} {_format_float(transformed[0][1])}']
        for x_value, y_value in transformed[1:]:
            commands.append(f'L {_format_float(x_value)} {_format_float(y_value)}')
        if is_closed:
            commands.append('Z')

        path_data = ' '.join(commands)
        path_lines.append(
            f'  <path d="{path_data}" fill="none" stroke="#000000" stroke-width="0.2" '
            f'stroke-linecap="round" stroke-linejoin="round" />'
        )

    if not path_lines:
        return False, tr('error_no_exportable_geometry')

    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" '
            f'width="{_format_float(width_mm)}mm" height="{_format_float(height_mm)}mm" '
            f'viewBox="0 0 {_format_float(width_mm)} {_format_float(height_mm)}">'
        ),
        *path_lines,
        '</svg>'
    ]

    with open(output_file, 'w', encoding='utf-8') as svg_file:
        svg_file.write('\n'.join(svg_lines))

    return True, ''


def _export_sketch_as_pdf(sketch: adsk.fusion.Sketch, output_file: str):
    export_data, error_message = _collect_export_strokes(sketch)
    if export_data is None:
        return False, error_message

    strokes = export_data['strokes']
    min_x = export_data['min_x']
    max_x = export_data['max_x']
    min_y = export_data['min_y']
    max_y = export_data['max_y']

    margin_mm = 5.0
    width_mm = (max_x - min_x) + (2.0 * margin_mm)
    height_mm = (max_y - min_y) + (2.0 * margin_mm)
    width_pt = width_mm * PDF_PT_PER_MM
    height_pt = height_mm * PDF_PT_PER_MM

    def map_x_pt(x_value):
        return ((x_value - min_x) + margin_mm) * PDF_PT_PER_MM

    def map_y_pt(y_value):
        return ((y_value - min_y) + margin_mm) * PDF_PT_PER_MM

    line_width_pt = 0.2 * PDF_PT_PER_MM
    content_lines = [
        f'{_format_float(line_width_pt)} w',
        '1 J',
        '1 j'
    ]

    for stroke in strokes:
        transformed = [(map_x_pt(x), map_y_pt(y)) for x, y in stroke]
        if len(transformed) < 2:
            continue

        is_closed = _points_close(transformed[0], transformed[-1], tolerance=0.001)
        if is_closed:
            transformed = transformed[:-1]
        if len(transformed) < 2:
            continue

        first_x, first_y = transformed[0]
        content_lines.append(f'{_format_float(first_x)} {_format_float(first_y)} m')
        for x_value, y_value in transformed[1:]:
            content_lines.append(f'{_format_float(x_value)} {_format_float(y_value)} l')
        if is_closed:
            content_lines.append('h')
        content_lines.append('S')

    content_stream = '\n'.join(content_lines) + '\n'
    content_bytes = content_stream.encode('ascii')
    content_length = len(content_bytes)

    objects = [
        '<< /Type /Catalog /Pages 2 0 R >>',
        '<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
        (
            f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {_format_float(width_pt)} {_format_float(height_pt)}] '
            f'/Resources << >> /Contents 4 0 R >>'
        ),
        f'<< /Length {content_length} >>\nstream\n{content_stream}endstream'
    ]

    pdf_data = bytearray()
    pdf_data.extend(b'%PDF-1.4\n')
    object_offsets = [0]

    for index, obj in enumerate(objects, start=1):
        object_offsets.append(len(pdf_data))
        pdf_data.extend(f'{index} 0 obj\n{obj}\nendobj\n'.encode('ascii'))

    xref_offset = len(pdf_data)
    pdf_data.extend(f'xref\n0 {len(objects) + 1}\n'.encode('ascii'))
    pdf_data.extend(b'0000000000 65535 f \n')
    for offset in object_offsets[1:]:
        pdf_data.extend(f'{offset:010d} 00000 n \n'.encode('ascii'))

    pdf_data.extend(
        (
            f'trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n'
            f'startxref\n{xref_offset}\n%%EOF\n'
        ).encode('ascii')
    )

    with open(output_file, 'wb') as pdf_file:
        pdf_file.write(pdf_data)

    return True, ''


def _export_sketch_as_dxf(sketch: adsk.fusion.Sketch, output_file: str):
    design = _get_active_design()
    if design is None:
        return False, tr('error_no_active_design')

    export_manager = design.exportManager
    if export_manager:
        try:
            options = export_manager.createDXFSketchExportOptions(output_file, sketch)
            if options and export_manager.execute(options):
                return True, ''
        except:
            pass

    try:
        if sketch.saveAsDXF(output_file):
            return True, ''
    except:
        pass

    return False, tr('error_dxf_export_failed')


def _export_selected_sketch(sketch: adsk.fusion.Sketch, output_dir: str, export_format: str):
    extension = export_format.lower()
    construction_name = _get_active_construction_name()
    sketch_name = _sanitize_filename(sketch.name)
    file_name = f'{construction_name}_{sketch_name}'
    output_file = os.path.join(output_dir, f'{file_name}.{extension}')

    if export_format == 'SVG':
        success, error_message = _export_sketch_as_svg(sketch, output_file)
    elif export_format == 'PDF':
        success, error_message = _export_sketch_as_pdf(sketch, output_file)
    else:
        success, error_message = _export_sketch_as_dxf(sketch, output_file)

    return success, output_file, error_message


def _collect_all_sketch_names():
    names = set()
    design = _get_active_design()
    if design is None:
        return names

    components = design.allComponents
    for i in range(components.count):
        component = components.item(i)
        if component is None:
            continue

        for j in range(component.sketches.count):
            sketch = component.sketches.item(j)
            if sketch and sketch.name:
                names.add(sketch.name)

    return names


def _next_export_sketch_name():
    existing_names = _collect_all_sketch_names()
    index = 1
    while True:
        candidate = f'{EXPORT_SKETCH_NAME_PREFIX}{index}'
        if candidate not in existing_names:
            return candidate
        index += 1


def _try_delete_sketch(sketch: adsk.fusion.Sketch):
    if sketch is None:
        return
    try:
        sketch.deleteMe()
    except:
        pass


def _project_face_edges_to_sketch(sketch: adsk.fusion.Sketch, face: adsk.fusion.BRepFace):
    if sketch is None or face is None:
        return False

    projected_edge_tokens = set()
    projected_any = False

    loops = getattr(face, 'loops', None)
    if loops is None:
        return False

    for i in range(loops.count):
        loop = loops.item(i)
        if loop is None:
            continue

        edges = getattr(loop, 'edges', None)
        if edges is None:
            continue

        for j in range(edges.count):
            edge = edges.item(j)
            if edge is None:
                continue

            temp_id = getattr(edge, 'tempId', None)
            edge_token = str(temp_id) if temp_id is not None else str(id(edge))
            if edge_token in projected_edge_tokens:
                continue
            projected_edge_tokens.add(edge_token)

            try:
                projection_result = sketch.project(edge)
                if projection_result and projection_result.count > 0:
                    projected_any = True
            except:
                pass

    if projected_any:
        return True

    try:
        projection_result = sketch.project(face)
        return bool(projection_result and projection_result.count > 0)
    except:
        return False


def _project_body_to_sketch(sketch: adsk.fusion.Sketch, face: adsk.fusion.BRepFace):
    if sketch is None or face is None:
        return False

    body = getattr(face, 'body', None)
    if body is None:
        return False

    native_body = None
    try:
        native_body = body.nativeObject
    except:
        native_body = None
    target_body = native_body if native_body else body

    try:
        projection_result = sketch.project(target_body)
        return bool(projection_result and projection_result.count > 0)
    except:
        return False


def _project_face_to_sketch(sketch: adsk.fusion.Sketch, face: adsk.fusion.BRepFace, projection_mode: str):
    if projection_mode == PROJECTION_MODE_BODIES:
        return _project_body_to_sketch(sketch, face)
    return _project_face_edges_to_sketch(sketch, face)


def _create_export_sketch_from_face(
    face: adsk.fusion.BRepFace,
    projection_mode: str = PROJECTION_MODE_SPECIFIED_OBJECTS
):
    if face is None or not face.isValid:
        return None, tr('error_no_valid_face')

    native_face = None
    try:
        native_face = face.nativeObject
    except:
        native_face = None
    target_face = native_face if native_face else face

    try:
        if adsk.core.Plane.cast(target_face.geometry) is None:
            return None, tr('error_no_valid_face')
    except:
        return None, tr('error_no_valid_face')

    target_component = None
    try:
        target_component = target_face.body.parentComponent if target_face.body else None
    except:
        target_component = None
    if target_component is None:
        return None, tr('error_face_sketch_create')

    new_sketch = None
    try:
        new_sketch = target_component.sketches.add(target_face)
    except:
        return None, tr('error_face_sketch_create')

    if new_sketch is None:
        return None, tr('error_face_sketch_create')

    try:
        new_sketch.name = _next_export_sketch_name()
    except:
        pass

    if not _project_face_to_sketch(new_sketch, target_face, projection_mode):
        _try_delete_sketch(new_sketch)
        return None, tr('error_face_projection')

    return new_sketch, ''


# Executed when add-in is run.
def start():
    # Recreate command definition so name/version updates are applied immediately.
    existing_def = ui.commandDefinitions.itemById(CMD_ID)
    if existing_def:
        existing_def.deleteMe()
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)
    if cmd_def is None:
        futil.log(f'{CMD_NAME}: {tr("error_command_definition")}', adsk.core.LogLevels.ErrorLogLevel)
        return

    # Define an event handler for the command created event. It will be called when the button is clicked.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******** Add a button into the UI so the user can run the command. ********
    # Get the target workspace the button will be created in.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    if workspace is None:
        futil.log(
            f'{CMD_NAME}: {tr("error_workspace_missing", workspace_id=WORKSPACE_ID)}',
            adsk.core.LogLevels.ErrorLogLevel
        )
        return

    # Remove stale controls from prior plugin locations.
    _cleanup_legacy_controls(workspace)

    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    if panel is None:
        panel = ui.allToolbarPanels.itemById(PANEL_ID)
    if panel is None:
        futil.log(
            f'{CMD_NAME}: {tr("error_panel_missing", panel_id=PANEL_ID)}',
            adsk.core.LogLevels.ErrorLogLevel
        )
        return

    # Recreate control in target panel.
    _remove_control_from_panel(panel)
    control = panel.controls.addCommand(cmd_def)

    # Specify if the command is promoted to the main toolbar.
    control.isPromoted = IS_PROMOTED
    try:
        control.isPromotedByDefault = IS_PROMOTED
    except:
        pass
    futil.log(f'{CMD_NAME}: {tr("log_started")}')


# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID) if workspace else None
    if panel is None:
        panel = ui.allToolbarPanels.itemById(PANEL_ID)
    command_control = panel.controls.itemById(CMD_ID) if panel else None
    command_definition = ui.commandDefinitions.itemById(CMD_ID)

    # Delete the button command control.
    if command_control:
        command_control.deleteMe()
    _cleanup_legacy_controls(workspace)

    # Delete the command definition.
    if command_definition:
        command_definition.deleteMe()


# Function that is called when a user clicks the corresponding button in the UI.
# This defines the contents of the command dialog and connects to command-related events.
def command_created(args: adsk.core.CommandCreatedEventArgs):
    global sketch_objects_by_label
    sketch_objects_by_label = {}

    inputs = args.command.commandInputs
    logo_input = _add_logo_input(inputs)
    if logo_input:
        try:
            logo_input.isFullWidth = True
        except:
            pass

    sketch_dropdown = inputs.addDropDownCommandInput(
        SKETCH_DROPDOWN_INPUT_ID,
        tr('label_sketches'),
        adsk.core.DropDownStyles.TextListDropDownStyle
    )

    sketch_entries = _collect_sketch_entries()
    if sketch_entries:
        sketch_dropdown.listItems.add(NO_SKETCH_SELECTED_TEXT, False)
        for index, entry in enumerate(sketch_entries):
            label, sketch = entry
            sketch_objects_by_label[label] = sketch
            sketch_dropdown.listItems.add(label, index == 0)
    else:
        sketch_dropdown.listItems.add(NO_SKETCHES_TEXT, True)
        sketch_dropdown.isEnabled = False

    face_selection_input = inputs.addSelectionInput(
        FACE_SELECTION_INPUT_ID,
        tr('label_faces'),
        tr('prompt_select_face')
    )
    face_selection_input.addSelectionFilter('PlanarFaces')
    face_selection_input.setSelectionLimits(0, 1)

    projection_mode_dropdown = inputs.addDropDownCommandInput(
        PROJECTION_MODE_DROPDOWN_INPUT_ID,
        tr('label_projection_mode'),
        adsk.core.DropDownStyles.TextListDropDownStyle
    )
    projection_mode_dropdown.listItems.add(tr('projection_mode_specified_objects'), True)
    projection_mode_dropdown.listItems.add(tr('projection_mode_bodies'), False)

    format_dropdown = inputs.addDropDownCommandInput(
        FORMAT_DROPDOWN_INPUT_ID,
        tr('label_export_format'),
        adsk.core.DropDownStyles.TextListDropDownStyle
    )
    format_dropdown.listItems.add('DXF', True)
    format_dropdown.listItems.add('SVG', False)
    format_dropdown.listItems.add('PDF', False)

    output_path_input = inputs.addStringValueInput(
        OUTPUT_PATH_INPUT_ID,
        tr('label_output_path'),
        _load_output_path()
    )
    try:
        output_path_input.isReadOnly = True
    except:
        pass

    inputs.addBoolValueInput(
        OUTPUT_PATH_BUTTON_INPUT_ID,
        tr('label_output_path_select'),
        False,
        '',
        False
    )

    inputs.addBoolValueInput(
        DEACTIVATE_SKETCH_INPUT_ID,
        tr('label_deactivate_sketch'),
        True,
        '',
        False
    )

    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.inputChanged, command_input_changed, local_handlers=local_handlers)
    futil.add_handler(args.command.validateInputs, command_validate_input, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)


def command_input_changed(args: adsk.core.InputChangedEventArgs):
    changed_input = args.input
    if changed_input.id == SKETCH_DROPDOWN_INPUT_ID:
        if _has_valid_sketch_selection(args.inputs):
            _clear_face_selection(args.inputs)
        return

    if changed_input.id == FACE_SELECTION_INPUT_ID:
        if _has_valid_face_selection(args.inputs):
            _set_sketch_dropdown_to_none(args.inputs)
        return

    if changed_input.id != OUTPUT_PATH_BUTTON_INPUT_ID:
        return

    browse_button = adsk.core.BoolValueCommandInput.cast(changed_input)
    if browse_button is None or not browse_button.value:
        return

    try:
        folder_dialog = ui.createFolderDialog()
        folder_dialog.title = tr('dialog_select_output_folder')
        current_path = _get_output_path(args.inputs)
        if current_path and os.path.isdir(current_path):
            try:
                folder_dialog.folder = current_path
            except:
                pass

        if folder_dialog.showDialog() == adsk.core.DialogResults.DialogOK:
            selected_path = folder_dialog.folder
            if selected_path:
                output_path_input = adsk.core.StringValueCommandInput.cast(args.inputs.itemById(OUTPUT_PATH_INPUT_ID))
                if output_path_input:
                    output_path_input.value = selected_path
                _persist_output_path(selected_path)
    finally:
        browse_button.value = False


def command_validate_input(args: adsk.core.ValidateInputsEventArgs):
    has_sketch_selection = _has_valid_sketch_selection(args.inputs)
    has_face_selection = _has_valid_face_selection(args.inputs)
    output_path = _get_output_path(args.inputs)
    selected_format = _get_selected_format(args.inputs)

    is_valid = has_sketch_selection or has_face_selection
    is_valid = is_valid and bool(output_path)
    is_valid = is_valid and selected_format in ('DXF', 'SVG', 'PDF')
    args.areInputsValid = is_valid


# This event handler is called when the user clicks the OK button in the command dialog.
def command_execute(args: adsk.core.CommandEventArgs):
    inputs = args.command.commandInputs
    selected_sketch = None
    created_sketch_from_face = False

    selected_face = _get_selected_face(inputs)
    if selected_face is not None:
        projection_mode = _get_selected_projection_mode(inputs)
        selected_sketch, create_error = _create_export_sketch_from_face(selected_face, projection_mode)
        if selected_sketch is None:
            ui.messageBox(create_error or tr('error_face_sketch_create'))
            return
        created_sketch_from_face = True
    else:
        selected_label = _get_selected_sketch_label(inputs)
        selected_sketch = _find_sketch_by_label(selected_label)
        if selected_sketch is None:
            ui.messageBox(tr('error_select_sketch_or_face'))
            return

    output_path = _get_output_path(inputs)
    if not output_path:
        ui.messageBox(tr('error_select_output_path'))
        return

    if not os.path.isdir(output_path):
        try:
            os.makedirs(output_path, exist_ok=True)
        except:
            ui.messageBox(tr('error_output_path_create', path=output_path))
            return

    _persist_output_path(output_path)

    export_format = _get_selected_format(inputs)
    success, output_file, error_message = _export_selected_sketch(selected_sketch, output_path, export_format)
    if success:
        if created_sketch_from_face and _get_deactivate_sketch_option(inputs):
            _deactivate_sketch_in_browser(selected_sketch)
        ui.messageBox(tr('msg_export_success', path=output_file))
    else:
        ui.messageBox(tr('msg_export_failed', export_format=export_format, error=error_message))


# This event handler is called when the command terminates.
def command_destroy(args: adsk.core.CommandEventArgs):
    global local_handlers
    local_handlers = []
