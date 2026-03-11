import adsk.core
import adsk.fusion
import json
import os
import re
import sys
from ...lib import fusionAddInUtils as futil
from ... import config
from ...version import VERSION

app = adsk.core.Application.get()
ui = app.userInterface


CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_cmdDialog'
CMD_NAME = f'SketchWizard {VERSION}'
CMD_Description = 'Exportiert eine Skizze als DXF, SVG oder PDF.'

# Specify that the command will be promoted to the panel.
IS_PROMOTED = False

# Konstruktion > Volumenkoerper > Erstellen
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
FORMAT_DROPDOWN_INPUT_ID = 'export_format_dropdown'
OUTPUT_PATH_INPUT_ID = 'output_path'
OUTPUT_PATH_BUTTON_INPUT_ID = 'output_path_button'

NO_SKETCHES_TEXT = 'Keine Skizzen in der Konstruktion vorhanden.'
SETTINGS_OUTPUT_PATH_KEY = 'output_path'
SETTINGS_FILENAME = 'settings.json'
SVG_STROKE_TOLERANCE_CM = 0.01  # 0.1 mm
PDF_PT_PER_MM = 72.0 / 25.4

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
            logo_input = inputs.addImageCommandInput(LOGO_IMAGE_INPUT_ID, 'Logo', candidate_path)
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


def _has_valid_sketch_selection(inputs: adsk.core.CommandInputs):
    sketch_dropdown = adsk.core.DropDownCommandInput.cast(inputs.itemById(SKETCH_DROPDOWN_INPUT_ID))
    if sketch_dropdown is None or not sketch_dropdown.isEnabled:
        return False
    if sketch_dropdown.selectedItem is None:
        return False
    return sketch_dropdown.selectedItem.name != NO_SKETCHES_TEXT


def _find_sketch_by_label(selected_label: str):
    if not selected_label:
        return None

    sketch = sketch_objects_by_label.get(selected_label)
    if sketch and sketch.isValid:
        return sketch

    for entry_label, entry_sketch in _collect_sketch_entries():
        if entry_label == selected_label:
            return entry_sketch
    return None


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


def _sanitize_filename(filename: str):
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', filename or '')
    cleaned = cleaned.strip().strip('.')
    return cleaned or 'sketch_export'


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
        return None, 'Die Skizze enthaelt keine exportierbaren Geometrien.'

    all_x = [point[0] for stroke in strokes for point in stroke]
    all_y = [point[1] for stroke in strokes for point in stroke]

    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)

    if _points_close((min_x, min_y), (max_x, max_y)):
        return None, 'Die Skizze hat keine gueltige Ausdehnung fuer den Export.'

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
        return False, 'Die Skizze enthaelt keine exportierbaren Geometrien.'

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
        return False, 'Es ist kein aktives Design vorhanden.'

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

    return False, 'DXF-Export fehlgeschlagen.'


def _export_selected_sketch(sketch: adsk.fusion.Sketch, output_dir: str, export_format: str):
    extension = export_format.lower()
    file_name = _sanitize_filename(sketch.name)
    output_file = os.path.join(output_dir, f'{file_name}.{extension}')

    if export_format == 'SVG':
        success, error_message = _export_sketch_as_svg(sketch, output_file)
    elif export_format == 'PDF':
        success, error_message = _export_sketch_as_pdf(sketch, output_file)
    else:
        success, error_message = _export_sketch_as_dxf(sketch, output_file)

    return success, output_file, error_message


# Executed when add-in is run.
def start():
    # Recreate command definition so name/version updates are applied immediately.
    existing_def = ui.commandDefinitions.itemById(CMD_ID)
    if existing_def:
        existing_def.deleteMe()
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)
    if cmd_def is None:
        futil.log(f'{CMD_NAME}: Command-Definition konnte nicht erstellt werden.', adsk.core.LogLevels.ErrorLogLevel)
        return

    # Define an event handler for the command created event. It will be called when the button is clicked.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******** Add a button into the UI so the user can run the command. ********
    # Get the target workspace the button will be created in.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    if workspace is None:
        futil.log(f'{CMD_NAME}: Workspace {WORKSPACE_ID} nicht gefunden.', adsk.core.LogLevels.ErrorLogLevel)
        return

    # Remove stale controls from prior plugin locations.
    _cleanup_legacy_controls(workspace)

    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    if panel is None:
        panel = ui.allToolbarPanels.itemById(PANEL_ID)
    if panel is None:
        futil.log(f'{CMD_NAME}: Ziel-Panel {PANEL_ID} nicht gefunden.', adsk.core.LogLevels.ErrorLogLevel)
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
    futil.log(f'{CMD_NAME}: gestartet')


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
        'Skizzen',
        adsk.core.DropDownStyles.TextListDropDownStyle
    )

    sketch_entries = _collect_sketch_entries()
    if sketch_entries:
        for index, entry in enumerate(sketch_entries):
            label, sketch = entry
            sketch_objects_by_label[label] = sketch
            sketch_dropdown.listItems.add(label, index == 0)
    else:
        sketch_dropdown.listItems.add(NO_SKETCHES_TEXT, True)
        sketch_dropdown.isEnabled = False

    format_dropdown = inputs.addDropDownCommandInput(
        FORMAT_DROPDOWN_INPUT_ID,
        'Exportformat',
        adsk.core.DropDownStyles.TextListDropDownStyle
    )
    format_dropdown.listItems.add('DXF', True)
    format_dropdown.listItems.add('SVG', False)
    format_dropdown.listItems.add('PDF', False)

    output_path_input = inputs.addStringValueInput(
        OUTPUT_PATH_INPUT_ID,
        'Ausgabepfad',
        _load_output_path()
    )
    try:
        output_path_input.isReadOnly = True
    except:
        pass

    inputs.addBoolValueInput(
        OUTPUT_PATH_BUTTON_INPUT_ID,
        'Ausgabepfad auswaehlen',
        False,
        '',
        False
    )

    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.inputChanged, command_input_changed, local_handlers=local_handlers)
    futil.add_handler(args.command.validateInputs, command_validate_input, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)


def command_input_changed(args: adsk.core.InputChangedEventArgs):
    changed_input = args.input
    if changed_input.id != OUTPUT_PATH_BUTTON_INPUT_ID:
        return

    browse_button = adsk.core.BoolValueCommandInput.cast(changed_input)
    if browse_button is None or not browse_button.value:
        return

    try:
        folder_dialog = ui.createFolderDialog()
        folder_dialog.title = 'Ausgabeordner auswaehlen'
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
    output_path = _get_output_path(args.inputs)
    selected_format = _get_selected_format(args.inputs)

    is_valid = has_sketch_selection
    is_valid = is_valid and bool(output_path)
    is_valid = is_valid and selected_format in ('DXF', 'SVG', 'PDF')
    args.areInputsValid = is_valid


# This event handler is called when the user clicks the OK button in the command dialog.
def command_execute(args: adsk.core.CommandEventArgs):
    inputs = args.command.commandInputs
    selected_label = _get_selected_sketch_label(inputs)
    selected_sketch = _find_sketch_by_label(selected_label)
    if selected_sketch is None:
        ui.messageBox('Es wurde keine gueltige Skizze ausgewaehlt.')
        return

    output_path = _get_output_path(inputs)
    if not output_path:
        ui.messageBox('Bitte waehlen Sie einen gueltigen Ausgabepfad aus.')
        return

    if not os.path.isdir(output_path):
        try:
            os.makedirs(output_path, exist_ok=True)
        except:
            ui.messageBox(f'Ausgabepfad kann nicht erstellt werden:\n{output_path}')
            return

    _persist_output_path(output_path)

    export_format = _get_selected_format(inputs)
    success, output_file, error_message = _export_selected_sketch(selected_sketch, output_path, export_format)
    if success:
        ui.messageBox(f'Export erfolgreich:\n{output_file}')
    else:
        ui.messageBox(f'Export fehlgeschlagen ({export_format}):\n{error_message}')


# This event handler is called when the command terminates.
def command_destroy(args: adsk.core.CommandEventArgs):
    global local_handlers
    local_handlers = []
