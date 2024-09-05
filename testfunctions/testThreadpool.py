import concurrent.futures
import time

def task(n):
    print(f"Task {n} starting")
    time.sleep(2)
    print(f"Task {n} completed")
    return n

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(task, i) for i in range(10)]
        
        for future in concurrent.futures.as_completed(futures):
            print(f"Result: {future.result()}")

if __name__ == '__main__':
    main()
