import os
import subprocess

def process_count(username: str):
    # количество процессов, запущенных из-под
    # текущего пользователя username
    try:
        output = subprocess.run(
            ['pgrep', '-u', username], stderr=subprocess.DEVNULL, stdout=subprocess.PIPE, text=True
        )
        return len(output.stdout.splitlines())
    except Exception as e:
        print(e)


def total_memory_usage(root_pid: int) -> float:
    # суммарное потребление памяти древа процессов
    # с корнем root_pid в процентах

    cmd = f"""
            total=$(grep MemTotal /proc/meminfo | awk '{{print $2}}')
            sum=$(ps -eo pid,ppid,rss | awk -v root={root_pid} '
                function s(p) {{ t=rss[p]; for(c in children[p]) t+=s(c); return t }}
                {{ rss[$1]=$3; children[$2][$1]=1 }}
                END {{ print s(root) }}
            ')
            echo "scale=2; $sum * 100 / $total" | bc
        """
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()
    return float(output) if output else 0.0


if __name__ == '__main__':
    print(process_count("luidvikovivanolegovich"))
    print(total_memory_usage(os.getpid()))

