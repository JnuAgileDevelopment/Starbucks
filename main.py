# coding:utf-8
import starbucks_ui
import sys

if __name__ == '__main__':
    # df = read_dataset('directory.csv')
    # # draw_groupby(df, 'Timezone', 'timezone')
    # # draw_groupby(df, 'Country', 'country')
    # # draw_country_map()
    # # draw_log_lat(df, 'Longitude', 'longitude')
    # # draw_log_lat(df, 'Latitude', 'latitude')
    # # print(df['Country'].value_counts())
    # draw.draw_timezone_map(df, "tz1")
    app = starbucks_ui.QApplication(sys.argv)
    ui = starbucks_ui.MyUI()
    sys.exit(app.exec_())

