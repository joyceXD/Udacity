from ugrow_features_util import *

# define UDFs for processing events data
bookmark = pfunc.udf(lambda event_list: value_in_list_ugrow('270', event_list), ptype.IntegerType())
card_created = pfunc.udf(lambda event_list: value_in_list_ugrow('260', event_list), ptype.IntegerType())
crash_occur = pfunc.udf(lambda event_list: value_in_list_ugrow('703', event_list), ptype.IntegerType())
discard_data = pfunc.udf(lambda event_list: value_in_list_ugrow('277', event_list), ptype.IntegerType())
error_technical = pfunc.udf(lambda event_list: value_in_list_ugrow('288', event_list), ptype.IntegerType())
error_user = pfunc.udf(lambda event_list: value_in_list_ugrow('289', event_list), ptype.IntegerType())
export_data = pfunc.udf(lambda event_list: value_in_list_ugrow('275', event_list), ptype.IntegerType())
market_optin = pfunc.udf(lambda event_list: value_in_list_ugrow('294', event_list), ptype.IntegerType())
market_optout = pfunc.udf(lambda event_list: value_in_list_ugrow('295', event_list), ptype.IntegerType())
notification_accept = pfunc.udf(lambda event_list: value_in_list_ugrow('283', event_list), ptype.IntegerType())
notification_decline = pfunc.udf(lambda event_list: value_in_list_ugrow('282', event_list), ptype.IntegerType())
reminder_optin = pfunc.udf(lambda event_list: value_in_list_ugrow('292', event_list), ptype.IntegerType())
reminder_optout = pfunc.udf(lambda event_list: value_in_list_ugrow('293', event_list), ptype.IntegerType())

# define UDFs for processing pagename data
get_page_name_type_udf = pfunc.udf(get_page_name_type, ptype.StringType())
get_error_message_type_udf = pfunc.udf(get_error_message_type, ptype.StringType())

# define UDFs for cleaning data
convert_to_date = pfunc.udf(parse_date_string, ptype.DateType())
get_time_zone_seconds_udf = pfunc.udf(get_time_zone_seconds, ptype.IntegerType())
process_first_visit_udf = pfunc.udf(process_first_visit, ptype.IntegerType())
process_missing_date_udf = pfunc.udf(process_missing_date, ptype.DateType())
unix_to_utc_datetime_udf = pfunc.udf(unix_to_utc_datetime, ptype.StringType())
validate_app_version_udf = pfunc.udf(validate_app_version, ptype.IntegerType())


# TODO: test this function with different event_list values
def extract_events(df):
    """ Extract certain events from the event list dataframe, and add columns corresponding to those events.
    :param df: data frame containing the event list column.
    :return: df with extra columns marking a 0 or 1 to indicate whether the event happened or not.
    """
    # if not df:
    # terminate_with_error(sc, extract_events.__name__)
    try:
        df = df.withColumn("event_list", pfunc.split(df.event_list, ",\s*"))
    except Exception as e:
        logging.error('extract_events(): Error with parsing values in post event list column: ' + str(e.message))
        # process event list with default value to handle this exception e.g. -1
        # TODO: test try exception block where event list is empty/incorrect format
        df = df.withColumn("event_list", pfunc.lit("-1"))
        return df

    df = df.withColumn('card_created', bookmark(df.event_list))
    df = df.withColumn('bookmark', bookmark(df.event_list))
    df = df.withColumn("export_data", export_data(df.event_list))
    df = df.withColumn("discard_data", discard_data(df.event_list))
    df = df.withColumn("notification_decline", notification_decline(df.event_list))
    df = df.withColumn("notification_accept", notification_accept(df.event_list))
    df = df.withColumn("technical_error", error_technical(df.event_list))
    df = df.withColumn("user_error", error_user(df.event_list))
    df = df.withColumn("reminder_optin", reminder_optin(df.event_list))
    df = df.withColumn("reminder_optout", reminder_optout(df.event_list))
    df = df.withColumn("remarketing_opt_in", market_optin(df.event_list))
    df = df.withColumn("remarketing_opt_out", market_optout(df.event_list))
    df = df.withColumn("crashes", crash_occur(df.event_list))

    return df


def change_column_types_visit_level(data):
    data = data.withColumn('visit_num', pfunc.col('visit_num').cast(ptype.IntegerType()))
    data = data.withColumn('days_since_first_use', pfunc.col('days_since_first_use').cast(ptype.IntegerType()))
    data = data.withColumn('days_since_last_use', pfunc.col('days_since_last_use').cast(ptype.IntegerType()))
    data = data.withColumn('time_taken_create_account', pfunc.col('time_taken_create_account').cast(ptype.DoubleType()))
    data = data.withColumn('technical_error', pfunc.col('technical_error').cast(ptype.IntegerType()))
    data = data.withColumn('user_error', pfunc.col('user_error').cast(ptype.IntegerType()))
    data = data.withColumn('remarketing_opt_in', pfunc.col('remarketing_opt_in').cast(ptype.IntegerType()))
    data = data.withColumn('remarketing_opt_out', pfunc.col('remarketing_opt_out').cast(ptype.IntegerType()))
    data = data.withColumn('crashes', pfunc.col('crashes').cast(ptype.IntegerType()))
    return data


def agg_per_visit_level(df):
    try:
        df_visit_level = df.groupBy(["visitor_id", "visit_num"]) \
            .agg(pfunc.min(df.date).alias('date'),
                 pfunc.min(df.hour).alias('hour'),
                 pfunc.min(df.date_time_tz).alias('visit_start'),
                 pfunc.max(df.date_time_tz).alias('visit_end'),
                 pfunc.first(df.first_launch_date).alias('first_launch_date'),
                 pfunc.max(df.days_since_first_use).alias('days_since_first_use'),
                 pfunc.max(df.days_since_last_use).alias('days_since_last_use'),
                 pfunc.first(df.country).alias('country'),
                 pfunc.first(df.city).alias('city'),
                 pfunc.max(pfunc.when(df.login_type == 'facebook', True)).alias('login_facebook'),
                 pfunc.max(pfunc.when(df.login_type == 'googleplus', True)).alias('login_google'),
                 pfunc.max(pfunc.when(df.login_type == 'myphilips', True)).alias('login_philips'),
                 pfunc.max(pfunc.when(df.login_type == 'None', True)).alias('login_other'),
                 pfunc.count(pfunc.when(df.page_name_type == 'article_view', True)).alias('page_count_article_view'),
                 pfunc.count(pfunc.when(df.page_name_type == 'coachmark_view', True))
                 .alias('page_count_coachmark_view'),
                 pfunc.count(pfunc.when(df.page_name_type == 'connected_devices_pair_baby-monitor', True))
                 .alias('page_count_connected_devices_pair_baby-monitor'),
                 pfunc.count(pfunc.when(df.page_name_type == 'connected_devices_pair_general', True))
                 .alias('page_count_connected_devices_pair_general'),
                 pfunc.count(pfunc.when(df.page_name_type == 'connected_devices_pair_thermometer', True))
                 .alias('page_count_connected_devices_pair_thermometer'),
                 pfunc.count(pfunc.when(df.page_name_type == 'library', True)).alias('page_count_library'),
                 pfunc.count(pfunc.when(df.page_name_type == 'menu', True)).alias('page_count_menu'),
                 pfunc.count(pfunc.when(df.page_name_type == 'onboarding', True)).alias('page_count_onboarding'),
                 pfunc.count(pfunc.when(df.page_name_type == 'profile', True)).alias('page_count_profile'),
                 pfunc.count(pfunc.when(df.page_name_type == 'registration', True)).alias('page_count_registration'),
                 pfunc.count(pfunc.when(df.page_name_type == 'settings', True)).alias('page_count_settings'),
                 pfunc.count(pfunc.when(df.page_name_type == 'tracker_add_edit_bottle', True))
                 .alias('page_count_tracker_add_edit_bottle'),
                 pfunc.count(pfunc.when(df.page_name_type == 'tracker_add_edit_breastfeed', True))
                 .alias('page_count_tracker_add_edit_breastfeed'),
                 pfunc.count(pfunc.when(df.page_name_type == 'tracker_add_edit_crying', True))
                 .alias('page_count_tracker_add_edit_crying'),
                 pfunc.count(pfunc.when(df.page_name_type == 'tracker_add_edit_diaper', True))
                 .alias('page_count_tracker_add_edit_diaper'),
                 pfunc.count(pfunc.when(df.page_name_type == 'tracker_add_edit_general', True))
                 .alias('page_count_tracker_add_edit_general'),
                 pfunc.count(pfunc.when(df.page_name_type == 'tracker_add_edit_length', True))
                 .alias('page_count_tracker_add_edit_length'),
                 pfunc.count(pfunc.when(df.page_name_type == 'tracker_add_edit_media', True))
                 .alias('page_count_tracker_add_edit_media'),
                 pfunc.count(pfunc.when(df.page_name_type == 'tracker_add_edit_moment', True))
                 .alias('page_count_tracker_add_edit_moment'),
                 pfunc.count(pfunc.when(df.page_name_type == 'tracker_add_edit_note', True))
                 .alias('page_count_tracker_add_edit_note'),
                 pfunc.count(pfunc.when(df.page_name_type == 'tracker_add_edit_pumping', True))
                 .alias('page_count_tracker_add_edit_pumping'),
                 pfunc.count(pfunc.when(df.page_name_type == 'tracker_add_edit_sleep', True))
                 .alias('page_count_tracker_add_edit_sleep'),
                 pfunc.count(pfunc.when(df.page_name_type == 'tracker_add_edit_temperature', True))
                 .alias('page_count_tracker_add_edit_temperature'),
                 pfunc.count(pfunc.when(df.page_name_type == 'tracker_add_edit_weight', True))
                 .alias('page_count_tracker_add_edit_weight'),
                 pfunc.count(pfunc.when(df.page_name_type == 'visualization_view_bottle', True))
                 .alias('page_count_visualization_view_bottle'),
                 pfunc.count(pfunc.when(df.page_name_type == 'visualization_view_breastfeed', True))
                 .alias('page_count_visualization_view_breastfeed'),
                 pfunc.count(pfunc.when(df.page_name_type == 'visualization_view_crying', True))
                 .alias('page_count_visualization_view_crying'),
                 pfunc.count(pfunc.when(df.page_name_type == 'visualization_view_diaper', True))
                 .alias('page_count_visualization_view_diaper'),
                 pfunc.count(pfunc.when(df.page_name_type == 'visualization_view_general', True))
                 .alias('page_count_visualization_view_general'),
                 pfunc.count(pfunc.when(df.page_name_type == 'visualization_view_humidity', True))
                 .alias('page_count_visualization_view_humidity'),
                 pfunc.count(pfunc.when(df.page_name_type == 'visualization_view_length', True))
                 .alias('page_count_visualization_view_length'),
                 pfunc.count(pfunc.when(df.page_name_type == 'visualization_view_media', True))
                 .alias('page_count_visualization_view_media'),
                 pfunc.count(pfunc.when(df.page_name_type == 'visualization_view_pumping', True))
                 .alias('page_count_visualization_view_pumping'),
                 pfunc.count(pfunc.when(df.page_name_type == 'visualization_view_sleep', True))
                 .alias('page_count_visualization_view_sleep'),
                 pfunc.count(pfunc.when(df.page_name_type == 'visualization_view_temperature', True))
                 .alias('page_count_visualization_view_temperature'),
                 pfunc.count(pfunc.when(df.page_name_type == 'visualization_view_weight', True))
                 .alias('page_count_visualization_view_weight'),
                 pfunc.max(df.time_taken_create_account).alias('time_taken_create_account'),
                 pfunc.countDistinct(df.card_id).alias('count_card_id'),
                 pfunc.sum(df.bookmark).alias('bookmark'),
                 pfunc.sum(df.export_data).alias('export_data'),
                 pfunc.sum(df.discard_data).alias('discard_data'),
                 pfunc.sum(df.notification_decline).alias('notification_decline'),
                 pfunc.sum(df.notification_accept).alias('notification_accept'),
                 pfunc.sum(df.technical_error).alias('technical_error'),
                 pfunc.sum(df.user_error).alias('user_error'),
                 pfunc.sum(df.reminder_optin).alias('reminder_optin'),
                 pfunc.sum(df.reminder_optout).alias('reminder_optout'),
                 pfunc.sum(df.remarketing_opt_in).alias('remarketing_opt_in'),
                 pfunc.sum(df.remarketing_opt_out).alias('remarketing_opt_out'),
                 pfunc.sum(df.crashes).alias('crashes')
                 )
        return df_visit_level

    except Exception as e:
        logging.exception(
            "Error while aggregating dataframe in {0}.".format(agg_per_visit_level.__name__))


def process_click_level_page_names(df):
    """ The page names contain many values. This function look at whether a user access certain pages.
    """
    df = df.withColumn('goals_view', goals_view_udf(pfunc.col('page_name')))
    df = df.withColumn('progress_view', progress_view_udf(pfunc.col('page_name')))
    df = df.withColumn('brush_head_view', brush_head_view_udf(pfunc.col('page_name')))
    df = df.withColumn('support_view', support_view_udf(pfunc.col('page_name')))
    df = df.withColumn('focus_areas_view', focus_areas_view_udf(pfunc.col('page_name')))
    df = df.withColumn('dental_view', dental_view_udf(pfunc.col('page_name')))
    df = df.withColumn('shop_view', shop_view_udf(pfunc.col('page_name')))
    return df


def process_click_level_segment_issues(df):
    """ Given a value of segment issues, in the format e.g. UPPER_RIGHT | LOWER_LEFT | UPPER_LEFT,
    return the number of segments having issues after brushing.
    :return: number of issue segments. In the above example it is 3.
    """
    df = df.withColumn('scrubbing_issues_segments',
                       pfunc.size(pfunc.split(df.scrubbing_issues_segments, '\|\s*')) - pfunc.lit(1))
    df = df.withColumn('coverage_issues_segments',
                       pfunc.size(pfunc.split(df.coverage_issues_segments, '\|\s*')) - pfunc.lit(1))
    df = df.withColumn('pressure_issues_segments',
                       pfunc.size(pfunc.split(df.pressure_issues_segments, '\|\s*')) - pfunc.lit(1))
    return df


def process_click_level_columns(df_proposition):
    try:
        df_proposition = df_proposition.withColumn('date', pfunc.to_date(df_proposition.timestamp))
        df_proposition = df_proposition.withColumn('hour', pfunc.hour(df_proposition.timestamp))
        df_proposition = df_proposition.withColumn('error_message',
                                                   process_handle_conn_error_udf(pfunc.col('error_message')))
        df_proposition = df_proposition.withColumn("error_message", blank_as_null("error_message"))
        df_proposition = df_proposition.withColumn("brushing_session_id", blank_as_null("brushing_session_id"))
        df_proposition = df_proposition.withColumn('notification_message_response',
                                                   process_notification_response_udf(
                                                       pfunc.col('notification_message_response')))
        df_proposition = df_proposition.withColumn('brushing_mode',
                                                   process_brushing_mode_udf(pfunc.col('brushing_mode')))
        df_proposition = df_proposition.withColumn('goal_name', process_goal_name_udf(pfunc.col('goal_name')))
        df_proposition = df_proposition.withColumn('coaching_notification',
                                                   get_coaching_msg_type_udf(
                                                       pfunc.col('coaching_notification')))
        df_proposition = process_click_level_segment_issues(df_proposition)
        df_proposition = process_click_level_page_names(df_proposition)
    except Exception as e:
        logging.exception(e.message)
    return df_proposition


def agg_features(df):
    try:
        df_dynamic_features = df.groupBy(["visitor_id"]) \
            .agg(
            pfunc.first(df.bundle_id).alias('bundle_id'),
            pfunc.first(df.first_launch_date).alias('first_launch_date'),
            pfunc.countDistinct(df.visit_number).alias('visit_count'),
            pfunc.avg(df.visit_duration).alias('avg_visit_duration'),
            pfunc.avg(df.coverage_issues_segments).alias('avg_coverage_issue'),
            pfunc.avg(df.scrubbing_issues_segments).alias('avg_scrubbing_issue'),
            pfunc.avg(df.pressure_issues_segments).alias('avg_pressure_issue'),
            pfunc.count(pfunc.when(df.coverage_issues_segments > 1, True)).alias('count_visit_coverage_issue'),
            pfunc.count(pfunc.when(df.scrubbing_issues_segments > 1, True)).alias('count_visit_scrubbing_issue'),
            pfunc.count(pfunc.when(df.pressure_issues_segments > 1, True)).alias('count_visit_pressure_issue'),
            pfunc.avg(df.error_message).alias('avg_errors'),
            pfunc.avg(df.tech_error).alias('avg_tech_error'),
            pfunc.avg(df.user_error).alias('avg_user_error'),
            pfunc.avg(df.crashes).alias('avg_crashes'),
            pfunc.sum(df.notification_message_response).alias('count_notification_response'),
            pfunc.max(df.handle_session_amount).alias('count_offline_sessions'),
            pfunc.count(pfunc.when(df.brushing_mode == 'clean', True)).alias('count_mode_clean'),
            pfunc.count(pfunc.when(df.brushing_mode == 'deep', True)).alias('count_mode_deep'),
            pfunc.count(pfunc.when(df.brushing_mode == 'gum', True)).alias('count_mode_gum'),
            pfunc.count(pfunc.when(df.brushing_mode == 'tongue', True)).alias('count_mode_tongue'),
            pfunc.count(pfunc.when(df.brushing_mode == 'white', True)).alias('count_mode_white'),
            pfunc.sum(df.brushing_session_id).alias('count_online_sessions'),
            pfunc.avg(df.brushing_complete_rate).alias('avg_brush_completion_rate'),
            pfunc.avg(df.coaching_typec).alias('avg_coaching_c'),
            pfunc.avg(df.coaching_typeg).alias('avg_coaching_g'),
            pfunc.avg(df.coaching_typep).alias('avg_coaching_p'),
            pfunc.avg(df.coaching_typem).alias('avg_coaching_m'),
            pfunc.count(pfunc.when(df.goal_name == 'custom_goal', True)).alias('count_custom_goal'),
            pfunc.count(pfunc.when(df.goal_name == 'fresh_breath', True)).alias('count_fresh_breath'),
            pfunc.count(pfunc.when(df.goal_name == 'gum_health', True)).alias('count_gum_health'),
            pfunc.count(pfunc.when(df.goal_name == 'plaque_removal', True)).alias('count_plaque_removal'),
            pfunc.count(pfunc.when(df.goal_name == 'whitening', True)).alias('count_whitening'),
            pfunc.avg(df.product_view).alias('avg_prod_view'),
            pfunc.max(df.product_registration_completed).alias('prod_registered'),
            pfunc.avg(df.service_requests).alias('avg_service_requests'),
            pfunc.sum(df.complete_goal).alias('sum_complete_goal'),
            pfunc.max(df.remarketing_opt_in).alias('marketing_opt_in'),
            pfunc.count(pfunc.when((df.hour >= 0) & (df.hour <= 11), True)).alias('count_visit_morning'),
            pfunc.count(pfunc.when((df.hour >= 12) & (df.hour <= 23), True)).alias('count_visit_evening'),
            pfunc.avg(df.goals_view_count).alias('avg_goals_view_count'),
            pfunc.avg(df.progress_view_count).alias('avg_progress_view_count'),
            pfunc.avg(df.brush_head_view_count).alias('avg_brush_head_view_count'),
            pfunc.avg(df.support_view_count).alias('avg_support_view_count'),
            pfunc.avg(df.focus_areas_view_count).alias('avg_focus_areas_view_count'),
            pfunc.avg(df.dental_view_count).alias('avg_dental_view_count'),
            pfunc.avg(df.shop_view_count).alias('avg_shop_view_count'),
            pfunc.max(df.days_since_first_use).alias('days_since_first_use'),
            pfunc.first(df.app_version).alias('app_version'),
            pfunc.first(df.mobile_device).alias('mobile_device'),
            pfunc.first(df.mobile_os_version).alias('mobile_os_version'),
            pfunc.first(df.city).alias('city'),
            pfunc.first(df.country).alias('country')
        )
        return df_dynamic_features
    except Exception as e:
        logging.exception(
            "Error while aggregating dataframe in {0}: {1}".format(agg_features.__name__, e.message))
        # terminate_with_error(sc, agg_features.__name__)
