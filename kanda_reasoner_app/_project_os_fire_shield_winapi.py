# project-path: kanda_reasoner_app/_project_os_fire_shield_winapi.py
"""Private stable Win32 primitives for Fire Shield OS worker isolation."""

from __future__ import annotations

import ctypes
import os
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Mapping, Sequence

from ctypes import wintypes

__all__: tuple[str, ...] = ()

ERROR_INSUFFICIENT_BUFFER = 122
ERROR_ALREADY_EXISTS = 183
EXTENDED_STARTUPINFO_PRESENT = 0x00080000
CREATE_UNICODE_ENVIRONMENT = 0x00000400
CREATE_SUSPENDED = 0x00000004
STARTF_USESTDHANDLES = 0x00000100
PROC_THREAD_ATTRIBUTE_SECURITY_CAPABILITIES = 0x00020009
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
JOB_OBJECT_EXTENDED_LIMIT_INFORMATION = 9
WAIT_OBJECT_0 = 0x00000000
WAIT_TIMEOUT = 0x00000102
INFINITE = 0xFFFFFFFF
SE_FILE_OBJECT = 1
DACL_SECURITY_INFORMATION = 0x00000004
GRANT_ACCESS = 1
REVOKE_ACCESS = 4
TRUSTEE_IS_SID = 0
TRUSTEE_IS_UNKNOWN = 0
NO_MULTIPLE_TRUSTEE = 0
SUB_CONTAINERS_AND_OBJECTS_INHERIT = 0x3
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
GENERIC_EXECUTE = 0x20000000
DELETE = 0x00010000


class WinApiIsolationError(RuntimeError):
    """Raised when one stable Windows isolation primitive fails."""


class _SidAndAttributes(ctypes.Structure):
    _fields_ = [("Sid", wintypes.LPVOID), ("Attributes", wintypes.DWORD)]


class _SecurityCapabilities(ctypes.Structure):
    _fields_ = [
        ("AppContainerSid", wintypes.LPVOID),
        ("Capabilities", ctypes.POINTER(_SidAndAttributes)),
        ("CapabilityCount", wintypes.DWORD),
        ("Reserved", wintypes.DWORD),
    ]


class _StartupInfoW(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("lpReserved", wintypes.LPWSTR),
        ("lpDesktop", wintypes.LPWSTR),
        ("lpTitle", wintypes.LPWSTR),
        ("dwX", wintypes.DWORD),
        ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD),
        ("dwYSize", wintypes.DWORD),
        ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD),
        ("cbReserved2", wintypes.WORD),
        ("lpReserved2", ctypes.POINTER(ctypes.c_ubyte)),
        ("hStdInput", wintypes.HANDLE),
        ("hStdOutput", wintypes.HANDLE),
        ("hStdError", wintypes.HANDLE),
    ]


class _StartupInfoExW(ctypes.Structure):
    _fields_ = [
        ("StartupInfo", _StartupInfoW),
        ("lpAttributeList", wintypes.LPVOID),
    ]


class _ProcessInformation(ctypes.Structure):
    _fields_ = [
        ("hProcess", wintypes.HANDLE),
        ("hThread", wintypes.HANDLE),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
    ]


class _TrusteeW(ctypes.Structure):
    pass


_TrusteeW._fields_ = [
    ("pMultipleTrustee", ctypes.POINTER(_TrusteeW)),
    ("MultipleTrusteeOperation", ctypes.c_int),
    ("TrusteeForm", ctypes.c_int),
    ("TrusteeType", ctypes.c_int),
    ("ptstrName", wintypes.LPWSTR),
]


class _ExplicitAccessW(ctypes.Structure):
    _fields_ = [
        ("grfAccessPermissions", wintypes.DWORD),
        ("grfAccessMode", ctypes.c_int),
        ("grfInheritance", wintypes.DWORD),
        ("Trustee", _TrusteeW),
    ]


class _JobBasicLimitInformation(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_longlong),
        ("PerJobUserTimeLimit", ctypes.c_longlong),
        ("LimitFlags", wintypes.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wintypes.DWORD),
        ("SchedulingClass", wintypes.DWORD),
    ]


class _IoCounters(ctypes.Structure):
    _fields_ = [
        ("ReadOperationCount", ctypes.c_ulonglong),
        ("WriteOperationCount", ctypes.c_ulonglong),
        ("OtherOperationCount", ctypes.c_ulonglong),
        ("ReadTransferCount", ctypes.c_ulonglong),
        ("WriteTransferCount", ctypes.c_ulonglong),
        ("OtherTransferCount", ctypes.c_ulonglong),
    ]


class _JobExtendedLimitInformation(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", _JobBasicLimitInformation),
        ("IoInfo", _IoCounters),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


def _dll(name: str):
    if os.name != "nt":
        raise WinApiIsolationError("OS_FIRE_SHIELD_WINDOWS_REQUIRED")
    dll = ctypes.WinDLL(name, use_last_error=True)
    lower = name.casefold()
    if lower == "kernel32.dll":
        dll.LocalFree.restype = wintypes.LPVOID
        dll.LocalFree.argtypes = [wintypes.LPVOID]
        dll.CreateFileW.restype = wintypes.HANDLE
        dll.CreateJobObjectW.restype = wintypes.HANDLE
        dll.ResumeThread.restype = wintypes.DWORD
        dll.WaitForSingleObject.restype = wintypes.DWORD
        dll.DeleteProcThreadAttributeList.restype = None
    if lower == "advapi32.dll":
        dll.FreeSid.restype = wintypes.LPVOID
        dll.FreeSid.argtypes = [wintypes.LPVOID]
    if lower == "userenv.dll":
        dll.CreateAppContainerProfile.restype = ctypes.c_long
        dll.DeriveAppContainerSidFromAppContainerName.restype = ctypes.c_long
        dll.DeleteAppContainerProfile.restype = ctypes.c_long
    return dll


def _check_bool(ok: int, marker: str) -> None:
    if not ok:
        raise WinApiIsolationError(
            f"{marker}:WINERROR={ctypes.get_last_error()}"
        )


def _set_trustee_sid(trustee: _TrusteeW, sid: wintypes.LPVOID) -> None:
    trustee.pMultipleTrustee = None
    trustee.MultipleTrusteeOperation = NO_MULTIPLE_TRUSTEE
    trustee.TrusteeForm = TRUSTEE_IS_SID
    trustee.TrusteeType = TRUSTEE_IS_UNKNOWN
    trustee.ptstrName = ctypes.cast(sid, wintypes.LPWSTR)


def _change_acl(path: Path, sid: wintypes.LPVOID, mode: int, mask: int) -> None:
    advapi = _dll("advapi32.dll")
    kernel = _dll("kernel32.dll")
    dacl = wintypes.LPVOID()
    descriptor = wintypes.LPVOID()
    result = advapi.GetNamedSecurityInfoW(
        str(path), SE_FILE_OBJECT, DACL_SECURITY_INFORMATION,
        None, None, ctypes.byref(dacl), None, ctypes.byref(descriptor),
    )
    if result != 0:
        raise WinApiIsolationError(
            f"OS_FIRE_SHIELD_GET_DACL_FAILED:{path}:{result}"
        )
    new_acl = wintypes.LPVOID()
    try:
        access = _ExplicitAccessW()
        access.grfAccessPermissions = mask
        access.grfAccessMode = mode
        access.grfInheritance = SUB_CONTAINERS_AND_OBJECTS_INHERIT
        _set_trustee_sid(access.Trustee, sid)
        result = advapi.SetEntriesInAclW(
            1, ctypes.byref(access), dacl, ctypes.byref(new_acl)
        )
        if result != 0:
            raise WinApiIsolationError(
                f"OS_FIRE_SHIELD_SET_ENTRIES_FAILED:{path}:{result}"
            )
        result = advapi.SetNamedSecurityInfoW(
            str(path), SE_FILE_OBJECT, DACL_SECURITY_INFORMATION,
            None, None, new_acl, None,
        )
        if result != 0:
            raise WinApiIsolationError(
                f"OS_FIRE_SHIELD_SET_DACL_FAILED:{path}:{result}"
            )
    finally:
        if new_acl:
            kernel.LocalFree(new_acl)
        if descriptor:
            kernel.LocalFree(descriptor)


@contextmanager
def acl_lease(path: Path, sid: wintypes.LPVOID, mask: int) -> Iterator[None]:
    """Grant one unique AppContainer SID lease and revoke it exactly."""
    _change_acl(path, sid, GRANT_ACCESS, mask)
    try:
        yield
    finally:
        _change_acl(path, sid, REVOKE_ACCESS, 0)


@contextmanager
def appcontainer_profile(name: str) -> Iterator[wintypes.LPVOID]:
    """Create one ephemeral profile and release its SID/profile afterward."""
    userenv = _dll("userenv.dll")
    advapi = _dll("advapi32.dll")
    sid = wintypes.LPVOID()
    hr = int(userenv.CreateAppContainerProfile(
        name, name, name, None, 0, ctypes.byref(sid)
    )) & 0xFFFFFFFF
    if hr & 0x80000000:
        if (hr & 0xFFFF) != ERROR_ALREADY_EXISTS:
            raise WinApiIsolationError(
                f"OS_FIRE_SHIELD_PROFILE_CREATE_FAILED:HRESULT=0x{hr:08X}"
            )
        hr = int(userenv.DeriveAppContainerSidFromAppContainerName(
            name, ctypes.byref(sid)
        )) & 0xFFFFFFFF
        if hr & 0x80000000:
            raise WinApiIsolationError(
                f"OS_FIRE_SHIELD_PROFILE_DERIVE_FAILED:HRESULT=0x{hr:08X}"
            )
    try:
        yield sid
    finally:
        if sid:
            advapi.FreeSid(sid)
        userenv.DeleteAppContainerProfile(name)


def _environment_block(env: Mapping[str, str]):
    entries = [f"{key}={value}" for key, value in sorted(env.items())]
    return ctypes.create_unicode_buffer("\0".join(entries) + "\0\0")


def open_inheritable_file(path: Path):
    """Open one binary capture file and return its inheritable Win32 handle."""
    import msvcrt

    stream = path.open("w+b")
    raw_handle = msvcrt.get_osfhandle(stream.fileno())
    os.set_handle_inheritable(raw_handle, True)
    handle = wintypes.HANDLE(raw_handle)
    return stream, handle


def open_null_input_handle():
    """Open inheritable Win32 NUL for child stdin."""
    kernel = _dll("kernel32.dll")
    generic_read = 0x80000000
    share_read = 0x00000001
    share_write = 0x00000002
    open_existing = 3
    inherit = wintypes.BOOL(True)

    class _SecurityAttributes(ctypes.Structure):
        _fields_ = [
            ("nLength", wintypes.DWORD),
            ("lpSecurityDescriptor", wintypes.LPVOID),
            ("bInheritHandle", wintypes.BOOL),
        ]

    attrs = _SecurityAttributes(ctypes.sizeof(_SecurityAttributes), None, inherit)
    handle = kernel.CreateFileW(
        "NUL", generic_read, share_read | share_write, ctypes.byref(attrs),
        open_existing, 0, None
    )
    if handle in (None, 0, wintypes.HANDLE(-1).value):
        raise WinApiIsolationError(
            f"OS_FIRE_SHIELD_NUL_OPEN_FAILED:WINERROR={ctypes.get_last_error()}"
        )
    return wintypes.HANDLE(handle)


def close_handle(handle) -> None:
    """Close one owned Win32 handle."""
    if handle:
        _dll("kernel32.dll").CloseHandle(handle)


def _configure_job(kernel):
    job = kernel.CreateJobObjectW(None, None)
    if not job:
        raise WinApiIsolationError(
            f"OS_FIRE_SHIELD_JOB_CREATE_FAILED:WINERROR={ctypes.get_last_error()}"
        )
    info = _JobExtendedLimitInformation()
    info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    _check_bool(
        kernel.SetInformationJobObject(
            job, JOB_OBJECT_EXTENDED_LIMIT_INFORMATION,
            ctypes.byref(info), ctypes.sizeof(info)
        ),
        "OS_FIRE_SHIELD_JOB_LIMIT_FAILED",
    )
    return job


def launch_appcontainer_process(
    *,
    argv: Sequence[str],
    cwd: Path,
    env: Mapping[str, str],
    timeout: float,
    sid: wintypes.LPVOID,
    stdout_handle: wintypes.HANDLE,
    stderr_handle: wintypes.HANDLE,
    stdin_handle: wintypes.HANDLE,
) -> tuple[int, bool]:
    """Launch one suspended AppContainer process, job it, then resume it."""
    kernel = _dll("kernel32.dll")
    attr_size = ctypes.c_size_t()
    kernel.InitializeProcThreadAttributeList(
        None, 1, 0, ctypes.byref(attr_size)
    )
    if ctypes.get_last_error() != ERROR_INSUFFICIENT_BUFFER:
        raise WinApiIsolationError("OS_FIRE_SHIELD_ATTRIBUTE_SIZE_FAILED")
    attr_buffer = ctypes.create_string_buffer(attr_size.value)
    attr_list = ctypes.cast(attr_buffer, wintypes.LPVOID)
    _check_bool(
        kernel.InitializeProcThreadAttributeList(
            attr_list, 1, 0, ctypes.byref(attr_size)
        ),
        "OS_FIRE_SHIELD_ATTRIBUTE_INIT_FAILED",
    )
    security = _SecurityCapabilities(sid, None, 0, 0)
    process = _ProcessInformation()
    startup = _StartupInfoExW()
    startup.StartupInfo.cb = ctypes.sizeof(startup)
    startup.StartupInfo.dwFlags = STARTF_USESTDHANDLES
    startup.StartupInfo.hStdInput = stdin_handle
    startup.StartupInfo.hStdOutput = stdout_handle
    startup.StartupInfo.hStdError = stderr_handle
    startup.lpAttributeList = attr_list
    _check_bool(
        kernel.UpdateProcThreadAttribute(
            attr_list, 0, PROC_THREAD_ATTRIBUTE_SECURITY_CAPABILITIES,
            ctypes.byref(security), ctypes.sizeof(security), None, None
        ),
        "OS_FIRE_SHIELD_ATTRIBUTE_SECURITY_FAILED",
    )
    job = wintypes.HANDLE()
    try:
        job = _configure_job(kernel)
        command_line = ctypes.create_unicode_buffer(subprocess.list2cmdline(argv))
        environment = _environment_block(env)
        flags = (
            EXTENDED_STARTUPINFO_PRESENT
            | CREATE_UNICODE_ENVIRONMENT
            | CREATE_SUSPENDED
        )
        _check_bool(
            kernel.CreateProcessW(
                str(argv[0]), command_line, None, None, True, flags,
                environment, str(cwd), ctypes.byref(startup.StartupInfo),
                ctypes.byref(process)
            ),
            "OS_FIRE_SHIELD_CREATE_PROCESS_FAILED",
        )
        _check_bool(
            kernel.AssignProcessToJobObject(job, process.hProcess),
            "OS_FIRE_SHIELD_ASSIGN_JOB_FAILED",
        )
        if kernel.ResumeThread(process.hThread) == 0xFFFFFFFF:
            raise WinApiIsolationError("OS_FIRE_SHIELD_RESUME_FAILED")
        wait_ms = (
            INFINITE if timeout <= 0
            else min(int(timeout * 1000), 0xFFFFFFFE)
        )
        wait = kernel.WaitForSingleObject(process.hProcess, wait_ms)
        timed_out = wait == WAIT_TIMEOUT
        if timed_out:
            kernel.TerminateJobObject(job, 124)
            kernel.WaitForSingleObject(process.hProcess, INFINITE)
        elif wait != WAIT_OBJECT_0:
            raise WinApiIsolationError(
                f"OS_FIRE_SHIELD_WAIT_FAILED:WINERROR={ctypes.get_last_error()}"
            )
        code = wintypes.DWORD()
        _check_bool(
            kernel.GetExitCodeProcess(process.hProcess, ctypes.byref(code)),
            "OS_FIRE_SHIELD_EXIT_CODE_FAILED",
        )
        return int(code.value), timed_out
    finally:
        if process.hThread:
            kernel.CloseHandle(process.hThread)
        if process.hProcess:
            kernel.CloseHandle(process.hProcess)
        if job:
            kernel.CloseHandle(job)
        kernel.DeleteProcThreadAttributeList(attr_list)
