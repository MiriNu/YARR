
# ----------------------


class DDA_calc:

    def __init__(self):
        self.coeff_player_pickup_item_ = 3
        self.coeff_spawn_height_and_timer = 0.1
        self.coeff_precision = 0.1
        self.coeff_speed_and_spawn_rate = 0.1

    # Avg pickup success rate
    def calc_threshold(self, player_pickup_item, player_spawn_item):
        pickup_success_rate = 0
        player_count = len(player_pickup_item)
        for i in player_pickup_item:
            for j in player_spawn_item:
                if j == 0:
                    pickup_success_rate += i / 0.001
                else:
                    pickup_success_rate += i/j
        #########
        """if self.coeff_player_pickup_item_ > 0.7:            
            self.coeff_player_pickup_item_ -= 0.01
            
        if self.coeff_spawn_height_and_timer < 0.3:  
            self.coeff_spawn_height_and_timer += 0.01
            self.coeff_precision += 0.01
            self.coeff_speed_and_spawn_rate += 0.01"""
        #########    
        print(self.coeff_player_pickup_item_,self.coeff_spawn_height_and_timer)    
        return pickup_success_rate / player_count

    def calc_spawn_height_and_timer(self, total_pickup_item, player_fall,
                                    player_pickup_item_fail,
                                    player_pickup_item, player_spawn_item):

        if player_spawn_item == 0:
            return 3

        abs_skill = abs((self.coeff_player_pickup_item_ * player_pickup_item) +
                        (self.coeff_spawn_height_and_timer *
                         (total_pickup_item - (player_fall / 2) -
                          (player_pickup_item_fail / 3))))
        rel_skill = abs_skill / player_spawn_item
        return rel_skill

    def calc_precision(self, player_avoid_damage,
                       player_get_damage, player_pickup_item,
                       player_spawn_item):

        if player_spawn_item == 0:
            return 2

        abs_skill = abs((self.coeff_player_pickup_item_ * player_pickup_item) +
                        (self.coeff_spawn_height_and_timer *
                         (player_avoid_damage - player_get_damage)))
        rel_skill = abs_skill / player_spawn_item
        return rel_skill

    def calc_speed_and_spawn_rate(self, player_avoid_damage, player_get_damage,
                                  player_block_damage, player_pickup_item,
                                  player_spawn_item):

        if player_spawn_item == 0:
            return 2

        abs_skill = abs((self.coeff_player_pickup_item_ * player_pickup_item) +
                        (self.coeff_spawn_height_and_timer *
                         (player_block_damage + (player_avoid_damage / 3) -
                          player_get_damage)))
        rel_skill = abs_skill / player_spawn_item
        return rel_skill
