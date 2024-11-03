"""
Rhythm tracker

Idea:
user inputs when they think beats are happening
and the program tracks how close they were to the actual beat
"""

import time
from pynput.keyboard import Key, Listener
from queue import Queue, Empty
import argparse

# TODO: queue of times we pressed the key
time_queue = Queue()

def on_press(key):
    """
    This function is called whenever a key is pressed.

    TODO: slap the time in the queue
    """
    print(key)
    time_queue.put(time.time())

def parse_args():
    """
    Parse command line arguments.
    Returns:
        args: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description='Rhythm tracking game')
    parser.add_argument('--bpm', type=int, default=30,
                       help='Beats per minute (default: 30)')
    parser.add_argument('--duration', type=int, default=60,
                       help='Duration of the game in seconds (default: 60)')
    
    return parser.parse_args()



def main():
    """
    This is the main function that runs the program.
    """
    # TODO: graphics!
    args = parse_args()
    bpm = args.bpm
    duration = args.duration
    listener = Listener(on_press=on_press)
    listener.start()
    # Calculate time between beats in seconds from BPM
    beat_interval = 60 / bpm
    
    # Get start time to track elapsed time
    start_time = time.time()
    
    # Initialize first beat time
    previous_beat_time = start_time
    next_beat_time = start_time + beat_interval
    print(f"{previous_beat_time=} {next_beat_time=}")
    # Run for specified duration
    while time.time() - start_time < duration:
        if time.time() >= next_beat_time:
            # Only update when we've passed the next beat
            previous_beat_time = next_beat_time
            next_beat_time += beat_interval
            print(f"{previous_beat_time=} {next_beat_time=}")

        # TODO: check if the time queue has any times in it
        try:
            hit_time = time_queue.get_nowait()
            # TODO: Do something with the hit_time
            # Calculate timing error relative to closest beat
            error_to_next = abs(hit_time - next_beat_time)
            error_to_prev = abs(hit_time - previous_beat_time)
            
            # Determine if hit was closer to previous or next beat
            # if we hit early, we want to return a negative number
            if error_to_next < error_to_prev:
                timing_error = error_to_next * -1
                target_beat = next_beat_time
            else:
                timing_error = error_to_prev
                target_beat = previous_beat_time
                
            print(f"Hit registered! Error: {timing_error:.3f} seconds from {target_beat}")
        except Empty:
            pass
            
        time.sleep(0.001)  # Small sleep to prevent maxing CPU
    
    print("Game over!")
    listener.stop()


if __name__ == "__main__":
    main()
