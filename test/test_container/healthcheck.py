import os

if not os.path.exists("count.txt"):
    with(open("count.txt", 'w')) as count:
        count.write("1")
    
with(open("count.txt", 'r+')) as count:
    run_count = int(count.read(1))
    if(run_count < 3):
        count.seek(0)
        count.write(f"{run_count + 1}")
        exit(0)
    else:
        count.seek(0)
        count.write(f"1")
        print("Drop down this container")
        exit(1)
