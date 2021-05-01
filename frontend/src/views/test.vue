```js
<template>
    <div>
        <v-switch
            v-model="spot"
            :label="$store.getters.spot ? 'SPOT' : 'NON SPOT'"
        ></v-switch>
    </div>
</template>

<script>
    export default {
        computed: {
            spot: {
                get() { return this.$store.getters.spot },
                set(value) { 
                    if(value == false){
                        if(confirm("Are you sure you would like to do this.")){
                            this.$store.commit('SET_SPOT', false);
                        } else { 
                            this.$store.commit('SET_SPOT', true);
                        }
                    } else { this.$store.commit('SET_SPOT', value); }
                }
            }
        },
    }
</script>
```

```
"vuetify": "^2.4.0",
"vuex": "^3.4.0"
```

Any idea why if I click on cancel in the confirm box the vuex state is correct (True) but the v-switch is False? 