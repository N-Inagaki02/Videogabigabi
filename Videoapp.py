import flet as ft
import cv2

def process_video(file_path: str, output_path: str = "output.mp4"):
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        print(f"動画ファイルを開けませんでした: {file_path}")
        return False

    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (360, 450), isColor=False)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        small = cv2.resize(frame, (12, 15), interpolation=cv2.INTER_LINEAR)
        pixelated = cv2.resize(small, (360, 450), interpolation=cv2.INTER_NEAREST)
        im_gray = cv2.cvtColor(pixelated, cv2.COLOR_BGR2GRAY)
        out.write(im_gray)

    cap.release()
    out.release()
    return True

def main(page: ft.Page):
    page.title = "動画ピクセル変換アプリ"
    page.padding = 30

    Column=ft.Column([ft.ProgressRing(), ft.Text("動画を処理中...")],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    dlg_success = ft.AlertDialog(
        modal=True,
        title=ft.Text("処理完了"),
        content=ft.Text("✅ 処理完了: output.mp4 に保存"),
        actions=[
            ft.TextButton("閉じる", on_click=lambda e: page.close(dlg_success)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Dialogを閉じた。処理完了。"),
    )

    dlg_miss = ft.AlertDialog(
        modal=True,
        title=ft.Text("処理失敗"),
        content=ft.Text("❌ 処理失敗"),
        actions=[
            ft.TextButton("Yes", on_click=lambda e: page.close(dlg_miss)),
            ft.TextButton("No", on_click=lambda e: page.close(dlg_miss)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Dialogを閉じた。処理失敗。"),
    )

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            page.add(Column)
            if process_video(file_path):
                #page.open(ft.SnackBar(ft.Text("✅ 処理完了: output.mp4 に保存")))
                page.remove(Column)
                page.open(dlg_success)
            else:
                #page.open(ft.SnackBar(ft.Text("❌ 処理失敗"), bgcolor=ft.colors.RED))
                page.remove(Column)
                page.open(dlg_miss)
        page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    page.add(
        ft.Text("mp4形式の動画を選択して、ピクセル加工を開始してください。"),
        ft.ElevatedButton("動画を選ぶ", on_click=lambda _: file_picker.pick_files(allow_multiple=False, allowed_extensions=["mp4"])),
    )

ft.app(target=main)