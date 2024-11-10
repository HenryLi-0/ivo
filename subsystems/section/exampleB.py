from subsystems.section.section import *

class SectionExampleB(Section):
    def render(state: State, im):
        '''Example B Area: `( 694,  22) to (1343, 675)` : size `( 650, 654)`'''
        img = im.copy()
        rmx = state.mx - 694
        rmy = state.my - 22

        choice = POINT_IDLE if random.random() > 0.5 else POINT_SELECTED
        for i in range(25):
            placeOver(img, choice, (math.cos((state.ticks/5+i/25))*250 + 325, math.sin((state.ticks/5+i/25))*250 + 327))
            placeOver(img, choice, (math.cos((state.ticks/2+i/25))*100 + 325, math.sin((state.ticks/2+i/25))*100 + 327))


        for id in state.ivos:
            if state.ivos[id][0] == "b":
                state.ivos[id][1].tick(img, state.interacting==id or ((state.lastInteraction==id) and (abs(time.time() - state.ivos[id][1].lastInteraction) < LAST_INTERACTION_KEY_TIME)), state.interacting==id)

        Section.overlayCrosshair(state, img, rmx, rmy)

        return img    
