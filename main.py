#!/usr/bin/python3

import time
from time import sleep
from playsound import playsound
from pythonosc import udp_client

import predictit
import prophet
import stts
import selenium_driver
import image_search

# Scheduler
starttime = time.time()

# Adding first person prophesizer seed to text generator
mood = "I, the prophet proclaim that"

# Web scrapper
driver = selenium_driver.SeleniumDriver()

# OSC client
client = udp_client.SimpleUDPClient("127.0.0.1", 3001)

while True:

    # ===========================================================================
    # Step 1: Retrieve bet headlines from PredictIt
    # ===========================================================================

    predictit.all_market_names()

    # ===========================================================================
    # Step 2: Pick random headline
    # ===========================================================================

    headline = predictit.pick_random_bet()
    # Send headline to openFrameworks 
    client.send_message("/headline", headline)
    print("====================================================================")
    print("HEADLINE: " + headline)
    print("====================================================================")

    # ===========================================================================
    # Step 3: Generate a prophecy
    # ===========================================================================
    prohecy = ""
    prophecy = prophet.generate_prophecy(headline + " " + mood)
    # Send prophecy to openframeworks
    client.send_message("/prophecy", prophecy)
    print("====================================================================")
    print("PROPHECY: " + "\n")
    print(prophecy)
    print("====================================================================")

    # ===========================================================================
    # Step 3: Speak prophecy aloud
    # ===========================================================================

    stts.synthesize(prophecy)
    playsound('tts.mp3')

    # ===========================================================================
    # Step 5: Find a nice image to accompany the prophecy
    # ===========================================================================

    image_search.find_image(headline)

    # ===========================================================================
    # Step 5: Record captcha input from human
    # ===========================================================================

    # Ask if human wants to share the prophecy
    playsound("./voice_interactions/share.mp3")
    playsound("beep.mp3")
    try:
        yesno = stts.hear(3)
    except:
        print("No answer")
        yesno = ""

    if "yes" in yesno:
        stts.record_human()

        # ===========================================================================
        # Step 6: Submit post to 8kun 
        # ===========================================================================
        try:
            driver.load_page()
            driver.write_to_subject(headline)
            driver.write_to_body(prohecy)
            driver.add_image()
            
            has_captcha = driver.get_captcha_image()
            
            if has_captcha:
                retry_captcha = 0
                while retry_captcha < 3:
                    try:
                        client.send_message("/captcha", True)
                        human_captcha = stts.record_human()
                        driver.fill_captcha(human_captcha)
                        driver.submit_captcha()
                    except:
                        retry_captcha += 1
                        playsound("./voice_interactions/failure.mp3")
            
            try:
                driver.submit_form()
                playsound("./voice_interactions/success.mp3")
            except:
                playsound("./voice_interactions/failure.mp3")
                break

        except:
            playsound("./voice_interactions/failure.mp3")
            break

    # Tell shrine screen to reload
    client.send_message("/reset", True)

    # Execute every 5 mins
    print("Returning in 5 minutes")
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
    
    # ===========================================================================