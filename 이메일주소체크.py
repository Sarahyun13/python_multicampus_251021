# 이메일 검사 예제 (re 모듈 사용)
import re

# 정규식 전체 설명:
# ^                     : 문자열 시작
# [A-Za-z0-9._%+-]+     : 로컬파트(local-part) - 영숫자 및 . _ % + - 문자가 하나 이상
# @                     : 반드시 하나의 @
# [A-Za-z0-9.-]+        : 도메인(하위 도메인들을 포함) - 영숫자, 점, 하이픈 허용 (하위 라벨이 점으로 구분)
# \.                    : 최상위 도메인(TLD) 앞의 점
# [A-Za-z]{2,}          : TLD - 영문자 2자 이상 (예: com, co.kr의 마지막 부분 등)
# $                     : 문자열 끝
# 주의: 이 정규식은 간단한 검증용이며 RFC 5322의 모든 경우(따옴표 포함 로컬파트, 국제화 도메인 등)는 처리하지 않음.

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def is_valid_email(email: str) -> bool:
    """이메일 형식 검증 (간단한 정규식 사용)

    동작:
    - 전체 문자열이 정규식과 일치하면 True 반환 (fullmatch 사용)
    - None 반환이 아닌 경우 True, 아니면 False

    제한 사항:
    - 로컬파트에 따옴표(")로 감싼 경우나 공백/특수문자 예외 케이스는 처리하지 않음.
    - 도메인에 국제화(비 ASCII) 문자는 처리하지 않음.
    - 실제 존재하는 이메일 주소(메일박스 유효성)는 확인하지 않음.
    """
    return bool(EMAIL_RE.fullmatch(email))

if __name__ == "__main__":
    # 검사할 샘플 10개
    samples = [
        "user@example.com",                    # valid - 기본 형태
        "user.name+tag@sub.example.co.kr",     # valid - + 태그, 서브도메인, 다중 TLD
        "user_name@mail-server.com",           # valid - 언더스코어, 하이픈 허용(로컬/도메인)
        "user@localhost",                      # invalid - TLD가 없음
        "user@.com",                           # invalid - 도메인 레이블이 비어 있음
        ".user@example.com",                   # invalid - 로컬파트가 점으로 시작
        "user@exam_ple.com",                   # invalid - 도메인에 언더스코어는 허용하지 않음
        "user@@example.com",                   # invalid - @가 두 개
        "user@example.c",                      # invalid - TLD가 한 글자 (최소 2자)
        "user@-example.com",                   # invalid - 도메인 레이블이 하이픈으로 시작
    ]

    for e in samples:
        print(f"{e:35} -> {'VALID' if is_valid_email(e) else 'INVALID'}")