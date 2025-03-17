import cv2

# 1. 비디오 소스 열기 (네트워크 스트림)
cap = cv2.VideoCapture(
    'http://210.99.70.120:1935/live/cctv001.stream/playlist.m3u8')
assert cap.isOpened(), 'Cannot open video stream'

# 2. VideoWriter 설정
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 30.0
default_fps = 30.0
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))
record_Mode = False

# 속도 조절을 위한 테이블 및 인덱스
speed_table = [1/2, 1, 1.5, 2, 3]
default_fps_index = 1
current_fps_index = default_fps_index
# 초기 fps는 speed_table 값을 사용 (여기서는 1)

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        break

    # 변경된 fps에 따라 wait_msec을 매번 업데이트
    wait_msec = int(1000 / fps)

    # 키 입력 처리: waitKey의 반환 값은 업데이트된 wait_msec을 기준으로 합니다.
    key = cv2.waitKey(wait_msec)

    if record_Mode:
        # 녹화 모드: 빨간 원 그리기 및 프레임 저장
        cv2.circle(frame, (30, 30), 15, (0, 0, 255), -1)
        out.write(frame)
    else:
        # 프리뷰 모드: 하얀 원 그리기
        cv2.circle(frame, (30, 30), 15, (255, 255, 255), -1)

    # 오른쪽에 FPS 및 배속 정보 텍스트 표시
    info = f'fps: {fps} (x{speed_table[current_fps_index]})'
    print(info)
    cv2.putText(frame, info, (30, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.imshow('frame', frame)

    # 키 이벤트 처리
    if key == 27:  # ESC: 종료
        break
    elif key == ord(' '):  # Space: 녹화/프리뷰 모드 전환
        record_Mode = not record_Mode
    elif key == ord('>') or key == ord('.'):  # 배속 증가
        current_fps_index = min(current_fps_index + 1, len(speed_table) - 1)
        fps = speed_table[current_fps_index] * default_fps
    elif key == ord('<') or key == ord(','):  # 배속 감소
        current_fps_index = max(current_fps_index - 1, 0)
        fps = speed_table[current_fps_index] * default_fps
    elif key == ord('\t'):
        current_fps_index = default_fps_index
        fps = default_fps
# 4. 리소스 정리
cap.release()
out.release()
cv2.destroyAllWindows()