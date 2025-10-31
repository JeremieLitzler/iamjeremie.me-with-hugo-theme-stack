public class UserCommentsQueryHandler: IRequestHandler <UserCommentsQuery, Paging<UserCommentResult>>
{
	private readonly UserService _userService;
	private readonly BookRespository _bookRepository;
	private readonly VideoGameRespository _videoGameRepository;
	public UserCommentsQueryHandler(UserService userService, BookRespository bookRepository, VideoGameRespository videoGameRepository)
	{
		_userService = userService;
		_bookRepository = bookRepository;
		_videoGameRepository = videoGameRepository;
	}

	public Task <Paging<UserCommentResult>> Handle(UserCommentsQuery request, CancellationToken cancellationToken)
	{
		var currentUser = _userService.GetUserProfileDetails();
		//BUG
		var elements = Extract<Book>(
			_bookRepository.GetEntities(), 
			currentUser,
			(media, comment) => new UserCommentResult
			{
				Title = media.BeneficiaryAccount,
					Author = media.Author,
					Comment = comment.Id.ToString(),
					CommentedBy = comment.Name,
					CommentCreatedOn = comment.CreatedOn,
			}).Union(Extract<VideoGame>(
				_videoGameRepository.GetEntities(), 
				currentUser,
				(media, comment) => new UserCommentResult
				{
					Title = media.BeneficiaryAccount,
						Author = media.Author,
						Comment = comment.Id.ToString(),
						CommentedBy = comment.Name,
				})
			);
		
		var searchResult = PerformSearch(elements, request.SearchText).OrderByDescending(item => item.CommentCreatedOn);
		var result = searchResult.Gridify(request.GridifyQuery);
		return Task.FromResult(result);
	}
	private IQueryable <UserCommentResult> Extract <T> (
        IQueryable <T> medias, 
        UserProfile currentUser, 
        Expression <Func<T, MediaComment, UserCommentResult>> mapper) where T: Media => 
        medias
            // Filter active medias by those which have a comment given by current user
            .Where(media => media.IsActive && media.comments.Any(comment => comment.CommentedBy == currentUser.Id))
            // Project the results from the comments and related media for each to build the list needed
            .SelectMany(media => 
                media.comments.Where(comment => comment.CommentedBy == currentUser.Id),
                mapper);

	private IQueryable <UserCommentResult> PerformSearch(IQueryable <UserCommentResult> results, string search) => 
        (search ?? "") // If null, set to empty string to return all results
	        .ToLower().Trim().Split(' ')
	        // Add "and" clauses to the query for each term
	        .Aggregate(results, (result, term) => result.Where(SearchExpression(term)));

	private readonly string _dateSeparator = "-";

	private Expression<Func<UserCommentResult, bool>> SearchExpression(string term) => 
        result => 
            (result.CommentCreatedOn.Year.ToString() + 
            _dateSeparator + 
            (result.CommentCreatedOn.Month > 10 ? result.CommentCreatedOn.Month.ToString() : "0" + result.CommentCreatedOn.Month.ToString()) +
             _dateSeparator + 
             (result.CommentCreatedOn.Day > 10 ? result.CommentCreatedOn.Day.ToString() : "0" + result.CommentCreatedOn.Day.ToString()) +
             _dateSeparator + 
             result.Title + 
             result.Author + 
             result.Comment + 
             result.CommentedBy + 
             result.CommentedBy).ToLower().Contains(term);
}