<template>
    <div :class="$vuetify.theme.dark ? 'knightrider-wrapper-dark' : 'knightrider-wrapper-light'">
        <span class="txt">{{ txt }}</span>
        <span :class="colorsss"></span>
        <span class="dodge"></span>
    </div>
</template>

<script>
    export default {
        name: 'knightrider',
        props: {
            txt: {
                type: String,
                default: "PyNance"
            },
        },
        computed: {
            colorsss() {
                if(this.$vuetify.theme.dark) { return 'gradient1'; }
                else { return 'gradient2'; }
            }
        },
    }
</script>

<style lang="scss" scoped>

@import url('https://fonts.googleapis.com/css?family=Orbitron:900&display=swap');

.knightrider-wrapper-dark {
    width: 100%;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #343a40;
}

.knightrider-wrapper-light {
    width: 100%;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #343a40;
}

.txtdiv-dark {
    background:#343a40;
    display: flex;
    align-items: center;
    width: 100%;
}

.txtdiv-light {
    background: #fdaeae;
    display: flex;
    align-items: center;
    width: 100%;
}

.txtspan {
    font-size: 12px;
}

.light {
    color:#000000;
}

.dark {
    color:#ffd8d8;
}

.txt {
    background:#343a40;
    font-family: 'Orbitron', sans-serif;
    font-size: 52px;
    color:#ffd8d8;
}

.txt::before {
    // content: 'Knight Rider';
    position: absolute;
    mix-blend-mode: difference;
    filter: blur(3px);
}

.knightrider-wrapper-dark, .knightrider-wrapper-light {
    // display: inline-flex;
    filter: brightness(200%);
    overflow: hidden;
}

.gradient1 {
    background: linear-gradient(115.8221404393721deg, rgba(245, 167, 128,1) 5.736111111111111%,rgba(241, 43, 92,1) 96.29166666666666%);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    mix-blend-mode: multiply;
}

.gradient2 {
    background: linear-gradient(115.8221404393721deg, rgb(128, 241, 245) 5.736111111111111%,rgb(79, 43, 241) 96.29166666666666%);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    mix-blend-mode: multiply;
}

.dodge {
    background: linear-gradient(white,black) center / 25% 25%;
    position: absolute;
    top:-100%;
    left:-100%;
    right:0;
    bottom:0;
    mix-blend-mode: color-dodge;
    animation: pulse1 3s linear infinite;
}

@keyframes pulse1 {
    to {
        transform: translate(25%,25%);
    }
    0% {
        opacity:0.1;
    }
    10% {
        opacity:0.8;
    }
    20% {
        opacity:0.5;
    }
    100% {
        opacity:0;
    }
}
</style>