import * as constants from '../constants';

function pageMode(state) {
  const topicsPages = [
    constants.PageNames.TOPICS_ROOT,
    constants.PageNames.TOPICS_CHANNEL,
    constants.PageNames.TOPICS_TOPIC,
    constants.PageNames.TOPICS_CONTENT,
  ];
  const learnPages = [constants.PageNames.RECOMMENDED, constants.PageNames.RECOMMENDED_CONTENT];
  const examPages = [constants.PageNames.EXAM_LIST, constants.PageNames.EXAM];
  if (topicsPages.some(page => page === state.pageName)) {
    return constants.PageModes.TOPICS;
  } else if (learnPages.some(page => page === state.pageName)) {
    return constants.PageModes.RECOMMENDED;
  } else if (constants.PageNames.SEARCH === state.pageName) {
    return constants.PageModes.SEARCH;
  } else if (examPages.some(page => page === state.pageName)) {
    return constants.PageModes.EXAM;
  }
  return undefined;
}

export { pageMode };
