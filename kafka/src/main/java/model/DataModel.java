package model;

import com.google.gson.annotations.SerializedName;
import java.io.Serializable;

public class DataModel implements Serializable {

//    @SerializedName("long_comments_num")
//    private long longComments;//长评数量
//    @SerializedName("short_comments_num")
//    private long shortComments;//短评数量
    @SerializedName("series_follow")
    private long followSeries;//追番人数
    @SerializedName("views")
    private long viewCnt;//新番总播放量
    @SerializedName("danmakus")
    private long danmakus;//弹幕数量
    @SerializedName("coins")
    private long coins;//投币
    @SerializedName("share")
    private long share;//分享
    @SerializedName("favorites")
    private long favorites;//收藏


    @Override
    public String toString() {
        return "DataModel{" +
                "followSeries=" + followSeries +
                ", viewCnt=" + viewCnt +
                ", danmakus=" + danmakus +
                ", coins=" + coins +
                ", share=" + share +
                ", favorites=" + favorites +
                '}';
    }


//    public long getLongComments() {
//        return longComments;
//    }
//
//    public void setLongComments(long longComments) {
//        this.longComments = longComments;
//    }
//
//    public long getShortComments() {
//        return shortComments;
//    }
//
//    public void setShortComments(long shortComments) {
//        this.shortComments = shortComments;
//    }

    public long getFollowSeries() {
        return followSeries;
    }

    public void setFollowSeries(long followSeries) {
        this.followSeries = followSeries;
    }

    public long getViewCnt() {
        return viewCnt;
    }

    public void setViewCnt(long viewCnt) {
        this.viewCnt = viewCnt;
    }
    public long getCoins() {
        return coins;
    }

    public void setCoins(long coins) {
        this.coins = coins;
    }

    public long getDanmakus() {
        return danmakus;
    }

    public void setDanmakus(long danmakus) {
        this.danmakus = danmakus;
    }

    public long getShare() {
        return share;
    }

    public void setShare(long share) {
        this.share = share;
    }

    public long getFavorites() {
        return favorites;
    }

    public void setFavorites(long favorites) {
        this.favorites = favorites;
    }
}
